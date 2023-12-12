# -*- coding: utf-8 -*-

from odoo import models, SUPERUSER_ID


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _send_invoice(self):
        '''To Invoice emails are triggered, this happens from the base
        '''
        template_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'sale.default_invoice_email_template',
            default=0
        ))
        if not template_id:
            return
        template = self.env['mail.template'].browse(template_id).exists()
        if not template:
            return

        for tx in self:
            print("\nTransaction: ",tx)
            tx = tx.with_company(tx.company_id).with_context(
                company_id=tx.company_id.id,
            )
            invoice_to_send = tx.invoice_ids.filtered(
                lambda i: not i.is_move_sent and i.state == 'posted' and i._is_ready_to_be_sent()
            )
            invoice_to_send.is_move_sent = True # Mark invoice as sent

            print("\nInvoice to send: ",invoice_to_send)
            
            subscription_products = tx.sale_order_ids.order_line.filtered(
                lambda line: line.product_template_id.recurring_invoice
            )
            if subscription_products:
                sub_template_id = self.env.ref(
                    "polaris_product_subscription.email_template_edi_invoice_for_subscription_product"
                ).id
                sub_template = self.env["mail.template"].browse(
                    int(sub_template_id)
                )
                module_attachments = []
                for line in subscription_products:
                    print("Subscription line: ",line)
                    """To store the generated api key inside the particular
                    sale order line with subscription product
                    """
                    api_key_file = line._generate_api_key(
                        tx, tx.partner_id
                    )
                    attachment = self.env["ir.attachment"].create(
                        {
                            "name": line.product_id.technical_name 
                            + ".zip" if line.product_id.technical_name else "",
                            "datas": line.product_id.module_zip if line.product_id.module_zip else "",
                            "res_model": "account.move",
                            "res_id": invoice_to_send.id if invoice_to_send.id else "",
                            "type": "binary",
                        }
                    )
                    module_attachments.append(attachment)
                    module_attachments.append(api_key_file)
                attachment_ids = [
                    (4, attach.id) for attach in module_attachments
                ]
                print('\nAttachment ids: ',attachment_ids,'\n')
                sub_template.attachment_ids = attachment_ids
                print("invoice to send: ",invoice_to_send,'\n')
                
                invoice_to_send.with_user(SUPERUSER_ID)._generate_pdf_and_send_invoice(sub_template)
                sub_template.attachment_ids = False
                return False
            else:
                print("\n++++++++Inside else\n")
                invoice_to_send.with_user(SUPERUSER_ID)._generate_pdf_and_send_invoice(template)
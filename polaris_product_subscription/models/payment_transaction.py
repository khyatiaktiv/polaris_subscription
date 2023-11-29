# -*- coding: utf-8 -*-

from odoo import models, SUPERUSER_ID


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    def _send_invoice(self):
        """Overwrite the whole  method as there is a for loop developed inside
        the function.
        """
        template_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("sale.default_invoice_email_template")
        )
        if not template_id:
            return
        template_id = int(template_id)
        template = self.env["mail.template"].browse(template_id)
        for tx in self:
            tx = tx.with_company(tx.company_id).with_context(
                company_id=tx.company_id.id,
            )
            invoice_to_send = tx.invoice_ids.filtered(
                lambda i: not i.is_move_sent
                and i.state == "posted"
                and i._is_ready_to_be_sent()
            )
            invoice_to_send.is_move_sent = True  # Mark invoice as sent
            for invoice in invoice_to_send:
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
                        """To store the generated api key inside the particular
                        sale order line with subscription product
                        """
                        api_key_file = line._generate_api_key(
                            tx, tx.partner_id
                        )
                        attachment = self.env["ir.attachment"].create(
                            {
                                "name": line.product_id.technical_name
                                + ".zip",
                                "datas": line.product_id.module_zip,
                                "res_model": "account.move",
                                "res_id": invoice.id,
                                "type": "binary",
                            }
                        )
                        module_attachments.append(attachment)
                        module_attachments.append(api_key_file)
                    attachment_ids = [
                        (4, attach.id) for attach in module_attachments
                    ]
                    lang = sub_template._render_lang(invoice.ids)[invoice.id]
                    model_desc_sub = invoice.with_context(lang=lang).type_name
                    # attachments not being added
                    invoice.with_context(
                        model_description=model_desc_sub,
                        attachment_ids=attachment_ids,
                    ).with_user(SUPERUSER_ID).message_post_with_template(
                        template_id=sub_template_id,
                        email_layout_xmlid="mail.mail_notification_layout_with_responsible_signature",
                    )
                else:
                    lang = template._render_lang(invoice.ids)[invoice.id]
                    model_desc = invoice.with_context(lang=lang).type_name
                    invoice.with_context(
                        model_description=model_desc
                    ).with_user(SUPERUSER_ID).message_post_with_template(
                        template_id=template_id,
                        email_layout_xmlid="mail.mail_notification_layout_with_responsible_signature",
                    )

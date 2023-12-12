# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.exceptions import AccessError, MissingError
from odoo.fields import Command
from odoo.http import request
from odoo.addons.sale_subscription.controllers import portal as subscription_portal

class SubscriptionPortal(subscription_portal.PaymentPortal):

    @http.route(['/my/subscriptions/<int:order_id>/resend_email_api_info'], type='http', auth="public")
    def subscription_resend_email_api_info(self, order_id, access_token=None, change_plan=False, **kw):
        print('\nsubscription_resend_email_api_info method called!!!!\n\n')
        order_sudo, redirection = self._get_subscription(access_token, order_id)
        print("\nOrder_sudo111 : ", order_sudo,'\n')
        if redirection:
            return redirection

        lang = request.env.context.get('lang')
        mail_template = request.env.ref('polaris_product_subscription.email_template_on_resend_api_details')
        print('\nMail Template')
        # if mail_template and mail_template.lang:
        #     lang = mail_template._render_lang(self.ids)[self.id]
        ctx = {
            'model': 'sale.order.line.api.key',
            'res_ids': order_sudo.ids,
            'template_id': mail_template.id if mail_template else None,
            'composition_mode': 'comment',
            'email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
        }

        request.env['mail.compose.message'].with_context(
            default_email_layout_xmlid='mail.mail_notification_layout_with_responsible_signature',
        ).create(ctx)._action_send_mail()











        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }









        # qs = ""
        # if change_plan:
        #     qs = "&change_plan=true"
        # if order_sudo.user_extend:
        #     renewal = order_sudo._create_renew_upsell_order('2_renewal', _('A renewal has been created by the client.'))
        #     renewal.action_quotation_sent()
        #     return request.redirect(renewal.get_portal_url(query_string=qs))


    @http.route(['/my/subscriptions/<int:order_id>/cancel_subscription'], type='http', auth="public")
    def cancel_subscription(self, order_id, access_token=None, change_plan=False, **kw):
        print("\ncancel subscriptions method called!!!!\n")
        order_sudo, redirection = self._get_subscription(access_token, order_id)
        print("\norder sudo222: ",order_sudo,'\n')
        if redirection:
            return redirection
        # qs = ""
        # if change_plan:
        #     qs = "&change_plan=true"
        # if order_sudo.user_extend:
        #     renewal = order_sudo._create_renew_upsell_order('2_renewal', _('A renewal has been created by the client.'))
        #     renewal.action_quotation_sent()
        #     re
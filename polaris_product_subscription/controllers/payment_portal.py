# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.exceptions import AccessError, MissingError
from odoo.fields import Command
from odoo.http import request
from odoo.addons.sale_subscription.controllers import portal as subscription_portal

class SubscriptionPortal(subscription_portal.PaymentPortal):

    # def display_success_notification(self):
   

    @http.route(['/my/subscriptions/<int:order_id>/resend_email_api_info'], type='http', auth="public")
    def subscription_resend_email_api_info(self, order_id, access_token=None, change_plan=False, **kw):
        print('\nsubscription_resend_email_api_info method called!!!!\n\n')
        order_sudo, redirection = self._get_subscription(access_token, order_id)
        print("\nOrder_sudo111 : ", order_sudo,'\n')
        if redirection:
            return redirection
        
        subr_history_object = request.env['sale.order.line.api.key']
        history_lines = subr_history_object.search([('order_id','in',order_sudo.ids)])
        print('\nHistory_lines: ',history_lines,'\n')

        for rec in history_lines:
            print("\nHistory record: ",rec,'\n')
            lang = request.env.context.get('lang')
            mail_template = request.env.ref('polaris_product_subscription.email_template_on_resend_api_details')
            print('\nMail Template: ',mail_template,'\n')

            ctx = {
                'email_layout_xmlid': "mail.mail_notification_light",
                'model': 'sale.order.line.api.key',
                'res_id': rec.id,
                'email_to': rec.customer_id and rec.customer_id.email or False,
            }
            try:
                mail_template.send_mail(rec.id, force_send=True,
                        raise_exception=True, email_values=ctx)
                return request.redirect(order_sudo.get_portal_url())
            except (UserError, ValidationError):
                raise UserError('Somehow Mail was not sent,Please try again later')

    @http.route(['/my/subscriptions/<int:order_id>/cancel_subscription'], type='http', auth="public")
    def cancel_subscription(self, order_id, access_token=None, change_plan=False, **kw):
        print("\ncancel subscriptions method called!!!!\n")
        order_sudo, redirection = self._get_subscription(access_token, order_id)
        print("\norder sudo222: ",order_sudo,'\n')
        if redirection:
            return redirection
        
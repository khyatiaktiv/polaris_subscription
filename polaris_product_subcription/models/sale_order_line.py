# -*- coding: utf-8 -*-
import secrets
import base64
from odoo import models, _, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    api_key = fields.Char(string='API Key')
    api_key_file = fields.Binary("API Key")
    api_key_filename = fields.Char(string='Filename', readonly=True)
    
    def action_open_api_key_view(self):
        lines = self.env["sale.order.line.api.key"].search([("order_line_id", "=", self.id)])
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "name": "API Keys",
            'res_model': 'sale.order.line.api.key',
            "domain": [("id", "in", lines.ids)],
            "target": "new",
            "res_id": (lines and len(lines) == 1) and lines.id or False,
        }

    def _generate_api_key(self):
        '''
        This method is used to generate a new api key for the Subscription Product
        purchased, therefore once the invoice is generated successfully the
        API key will be created and stored in the particular Sale Order
        Line and in the History for internal use.
        '''
        print("\ngenerate api key method called")
        sale_order_line_api_key_obj = self.env['sale.order.line.api.key']
        generated_key = secrets.token_urlsafe(16)
        message = f"Key: 'polaris.{self.product_id.technical_name}.auth_code' \nValue: '{generated_key}'"
        self.api_key = generated_key
        vals = {
            'order_line_id' : self.id,
            'product_id': self.product_id.id,
            'api_key' : self.api_key,
            'status' : 'start'
        }
        print("sale history key: ",vals,'\n')
        sale_order_line_api_key_obj.create(vals)

        # new_attach = self.env['ir.attachment'].create({
        #     'datas': base64.b64encode(message.encode()),
        #     'mimetype': 'text/plain',
        #     'name': f'{self.name}.txt',
        # })
        # self.api_key_file = new_attach

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
        # generated_key = secrets.token_urlsafe(16)
        # message = f"Key: 'polaris.{self.product_id.technical_name}.auth_code' \nValue: '{generated_key}'"
        # new_attach = self.env['ir.attachment'].create({
        #     'datas': base64.b64encode(message.encode()),
        #     'mimetype': 'text/plain',
        #     'name': f'{self.name}.txt',
        # })
        # # self.api_key_file = new_attach
        # self.api_key = generated_key
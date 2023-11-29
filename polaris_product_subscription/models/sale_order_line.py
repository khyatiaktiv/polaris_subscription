# -*- coding: utf-8 -*-
import secrets
import base64
from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    api_key = fields.Char(string="API Key")

    def action_open_api_key_view(self):
        lines = self.env["sale.order.line.api.key"].search(
            [("order_line_id", "=", self.id)]
        )
        return {
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "name": "API Keys",
            "res_model": "sale.order.line.api.key",
            "domain": [("id", "in", lines.ids)],
            "target": "new",
            "res_id": (lines and len(lines) == 1) and lines.id or False,
        }

    def _generate_api_key(self, transaction_id, customer_id):
        """
        This method is used to generate a new api key for the Subscription
        Product purchased, therefore once the invoice is generated successfully
        the API key will be created and stored in the particular Sale Order
        Line and in the History for internal use.
        """
        sale_order_line_api_key_obj = self.env["sale.order.line.api.key"]
        generated_key = secrets.token_urlsafe(16)
        message = (
            f"Key: 'polaris.{self.product_id.technical_name}.auth_code'"
            f"\nValue: '{generated_key}'"
        )
        self.api_key = generated_key
        vals = {
            "order_line_id": self.id,
            "product_id": self.product_id.id,
            "api_key": self.api_key,
            "status": "start",
            "transaction_id": transaction_id.id,
            "customer_id": customer_id.id,
            "key_expiration_date": self.order_id.next_invoice_date,
        }
        sale_order_line_api_key_obj.create(vals)
        new_attach = self.env["ir.attachment"].create(
            {
                "datas": base64.b64encode(message.encode()),
                "mimetype": "text/plain",
                "name": f"{self.product_id.technical_name}.txt",
            }
        )
        return new_attach

# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleOrderLineApiKey(models.Model):
    _name = "sale.order.line.api.key"
    _description = "Sale Order Line API Key"
    _rec_name = "technical_name"

    customer_id = fields.Many2one("res.partner", string="Customer")
    order_line_id = fields.Many2one("sale.order.line", string="Order Line")
    order_id = fields.Many2one("sale.order",related='order_line_id.order_id')
    product_id = fields.Many2one("product.product", string="Product")
    technical_name = fields.Char(related="product_id.technical_name")
    api_key = fields.Char(string="API Key")
    status = fields.Selection(
        [
            ("start", "Start"),
            ("inprogress", "In Progress"),
            ("stop", "Stop"),
            ("resume", "Resume"),
        ]
    )
    transaction_id = fields.Many2one(
        "payment.transaction", string="Payment Transaction"
    )
    client_domain = fields.Char(string="Client Domain")
    key_expiration_date = fields.Date(string="Key Expiration date")

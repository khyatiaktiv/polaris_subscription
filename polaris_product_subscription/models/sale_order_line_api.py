# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrderLineApiKey(models.Model):
    _name = 'sale.order.line.api.key'
    _description = "Sale Order Line API Key"
    _rec_name = 'product_name'
    
    customer_id = fields.Many2one('res.partner', string='Partner')
    order_line_id = fields.Many2one("sale.order.line", string="SO Line")
    product_id = fields.Many2one("product.product", string="Product")
    product_name = fields.Char(related='product_id.name')
    api_key = fields.Char(string="API Key")
    status = fields.Selection([
        ("draft", "Draft"),
        ("start", "Start"),
        ("inprogress", "In Progress"),
        ("stop", "Stop"),
        ("resume", "Resume"),
    ])
    transaction_id = fields.Many2one('payment.transaction',string="Payment Transaction")
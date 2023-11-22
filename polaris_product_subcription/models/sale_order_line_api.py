# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLineApiKey(models.Model):
    _name = 'sale.order.line.api.key'
    _description = "Sale Order Line API Key"
    
    order_line_id = fields.Many2one("sale.order.line", string="SO Line")
    product_id = fields.Many2one("product.product", string="Product")
    api_key = fields.Char(string="API Key")
    status = fields.Selection([
        ("draft", "Draft"),
        ("start", "Start"),
        ("inprogress", "In Progress"),
        ("stop", "Stop"),
        ("resume", "Resume"),
    ])

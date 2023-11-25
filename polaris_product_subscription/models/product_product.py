# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    clone_url = fields.Char("Clone URL")
    document_link = fields.Char("Document Link")
    technical_name = fields.Char("Technical Module Name")
    module_zip = fields.Binary("Module Zip")


class ProductProduct(models.Model):
    _inherit = 'product.template'

    clone_url = fields.Char("Clone URL")
    document_link = fields.Char("Document Link")
    technical_name = fields.Char("Technical Module Name")
    
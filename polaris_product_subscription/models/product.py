# -*- coding: utf-8 -*-

import base64
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    clone_url = fields.Char("Clone URL")
    document_link = fields.Char("Document Link")
    technical_name = fields.Char("Technical Module Name")
    module_zip = fields.Binary("Module Zip")
    filename = fields.Char("File Name")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    clone_url = fields.Char(
        "Clone URL",
        compute="_compute_module_details",
        inverse="_set_module_details",
        store=True,
    )
    document_link = fields.Char(
        "Document Link",
        compute="_compute_module_details",
        inverse="_set_module_details",
        store=True,
    )
    technical_name = fields.Char(
        "Technical Module Name",
        compute="_compute_module_details",
        inverse="_set_module_details",
        store=True,
    )
    module_zip = fields.Binary(
        "Module Zip",
        compute="_compute_module_details",
        inverse="_set_module_details",
        store=True,
    )
    filename = fields.Char(
        "File Name",
        compute="_compute_module_details",
        inverse="_set_module_details",
        store=True,
    )

    @api.depends(
        "product_variant_ids",
        "product_variant_ids.clone_url",
        "product_variant_ids.document_link",
        "product_variant_ids.technical_name",
        "product_variant_ids.module_zip",
        "product_variant_ids.filename",
    )
    def _compute_module_details(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1
        )
        for template in unique_variants:
            template.clone_url = template.product_variant_ids.clone_url
            template.document_link = template.product_variant_ids.document_link
            template.technical_name = (
                template.product_variant_ids.technical_name
            )
            template.module_zip = (
                base64.b64encode(template.product_variant_ids.module_zip)
                if template.product_variant_ids.module_zip
                else False
            )
            template.filename = (
                template.product_variant_ids.filename
                if template.product_variant_ids.filename
                else False
            )
        for template in self - unique_variants:
            template.clone_url = False
            template.document_link = False
            template.technical_name = False
            template.module_zip = False
            template.filename = False

    def _set_module_details(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.clone_url = template.clone_url
                template.product_variant_ids.document_link = (
                    template.document_link
                )
                template.product_variant_ids.technical_name = (
                    template.technical_name
                )
                template.product_variant_ids.module_zip = (
                    base64.b64encode(template.module_zip)
                    if template.module_zip
                    else False
                )
                template.product_variant_ids.filename = (
                    template.filename if template.filename else False
                )

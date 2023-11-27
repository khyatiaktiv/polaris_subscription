# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    x_module_expiration_date = fields.Datetime("Expiration Date")
    x_module_api_key = fields.Char("API Key")
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            x_module_expiration_date=params.get_param('polaris_product_subscription.x_module_expiration_date'),
            x_module_api_key=params.get_param('polaris_product_subscription.x_module_api_key')
        )
        return res
    
    def set_values(self):
        super().set_values()
        IrConfigParameter = self.env['ir.config_parameter'].sudo()
        IrConfigParameter.set_param("polaris_product_subscription.x_module_expiration_date", self.x_module_expiration_date)
        IrConfigParameter.set_param("polaris_product_subscription.x_module_api_key", self.x_module_api_key)
        
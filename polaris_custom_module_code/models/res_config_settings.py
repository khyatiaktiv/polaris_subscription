# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    polaris_custom_module_code_api_key = fields.Char(
        "Polaris Custom Module Code API Key"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()
        res.update(
            polaris_custom_module_code_api_key=params.get_param(
                "polaris_custom_module_code.polaris_custom_module_code_api_key"
            ),
        )
        return res

    def set_values(self):
        super().set_values()
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        IrConfigParameter.set_param(
            "polaris_custom_module_code.polaris_custom_module_code_api_key",
            self.polaris_custom_module_code_api_key,
        )

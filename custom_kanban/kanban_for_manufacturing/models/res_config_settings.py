# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """Class inherit for adding some configuration."""

    _inherit = 'res.config.settings'

    internal_transfer_kanban_id = fields.Many2one(
        string="Internal Transfer Type for Kanban",
        related='company_id.internal_transfer_kanban_id', readonly=False)
        
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

    def validate_api_details(self):
        print('\nValidate API details method called')
        http_obj = self.env['ir.http'].connect_to_odoo_server_polaris_custom_module_code()
# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    """Class inherit for adding some configuration."""

    _inherit = 'res.config.settings'

    internal_transfer_kanban_id = fields.Many2one(
        string="Internal Transfer Type for Kanban",
        related='company_id.internal_transfer_kanban_id', readonly=False)
        
    polaris_custom_module_code_api_key = fields.Char(
        "Polaris Custom Module Code API Key", readonly=True
    )

    api_key_validated = fields.Selection([
                                        ('not_validated','API Key Not Validated'),
                                        ('successful','API Key Validated Successfully'),
                                        ('unsuccessful',"API Validation Unsuccessful")],
                                        default=lambda self: self.env['ir.config_parameter'].get_param('api_key_validated'))

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env["ir.config_parameter"].sudo()

        res.update(
            polaris_custom_module_code_api_key=params.get_param(
                "kanban_for_manufacturing.polaris_custom_module_code_api_key"
            ),
        )
        return res

    def set_values(self):
        super().set_values()
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        IrConfigParameter.set_param(
            "kanban_for_manufacturing.polaris_custom_module_code_api_key",
            self.polaris_custom_module_code_api_key)


    def validate_api_details(self):
        http_obj = self.env['ir.http'].connect_to_odoo_server_polaris_custom_module_code()
        if http_obj['result']['status']== 'invalid_key':
            kanban_group = self.env.ref('kanban_for_manufacturing.group_kanban_manufacturing_user')
            kanban_group.write({'users': [(5, self.env.user.id)]})
            raise ValidationError('The Validation Api key is Either wrong or Has Expired. Please try to validate again or Contact your Administratator!')
        else:
            kanban_group = self.env.ref('kanban_for_manufacturing.group_kanban_manufacturing_user')
            kanban_group.write({'users': [(4, self.env.user.id)]})
            return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": 'success',
                "title": 'Connection Successful',
                "message": 'API Validated Succesful',
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            }
            }
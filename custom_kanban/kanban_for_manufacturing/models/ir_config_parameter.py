from odoo import models

class IrConfigParameterX(models.Model):
    _inherit = 'ir.config_parameter'

    def write(self,vals):
        if 'value' in vals:
            new_value = vals['value']
            old_value = self.value
    
            old_api_value_rec_id = self.search([('key','=','kanban_for_manufacturing.polaris_custom_module_code_api_key_before')]).id
            
            if new_value != old_value:
                kanban_group = self.env.ref('kanban_for_manufacturing.group_kanban_manufacturing_user')
                kanban_group.write({'users': [(5, self.env.user.id)]})

            self._cr.execute(
            """
            UPDATE ir_config_parameter SET value = %s
            WHERE id = %s
            """,(old_value, old_api_value_rec_id))
        
        res = super(IrConfigParameterX,self).write(vals)
        return res

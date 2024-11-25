from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit="mrp.production"
    _name="mrp.production"

    def action_open_on_demand_quality_check(self):
        self.ensure_one()
        if self.state in ['draft', 'done', 'cancel']:
            raise UserError(_('You can not create quality check for a draft, done or cancelled manufacturing order.'))
        return {
            'name': _('On-Demand Quality Check'),
            'type': 'ir.actions.act_window',
            'res_model': 'quality.check.on.demand',
            'views': [(self.env.ref('impress_qc_on_demand.quality_check_on_demand_view_form').id, 'form')],
            'target': 'new',
            'context': {
                'default_production_id': self.id,
                'on_demand_wizard': True,
            }
        }
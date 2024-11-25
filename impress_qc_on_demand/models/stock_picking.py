from odoo import models, fields, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"
    _name = "stock.picking"

    test_field = fields.Char('Test field')

    def action_open_on_demand_quality_check(self):
        self.ensure_one()
        if self.state in ['draft', 'done', 'cancel']:
            raise UserError(_('You can not create quality check for a draft, done or cancelled transfer.'))
        return {
            'type': 'ir.actions.act_window',
            'name': _('On-Demand Quality Check'),
            'res_model': 'quality.check.on.demand',
            'views': [(self.env.ref('impress_qc_on_demand.quality_check_on_demand_view_form').id, 'form')],
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'on_demand_wizard': True,
            }
        }
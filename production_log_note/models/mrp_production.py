# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    log_note = fields.Text(string="Log Note")

    def action_log_note(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'res_model': 'mrp.production',
            'views': [[self.env.ref('mrp_workorder.mrp_production_view_form_log_note').id, 'form']],
            'name': _('Add log note'),
            'target': 'new',
            'context': {
                'default_production_id': self.id,
            }
        }
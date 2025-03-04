# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
_logger = logging.getLogger(__name__)


class LogMixin(models.Model):
    _name = 'log.mixin'
    _description = 'log.mixin'

    name = fields.Char('Name')
    signature = fields.Binary('Signature')

    quality_check_id = fields.Many2one('quality.check', 'Quality Check')
    production_id = fields.Many2one('mrp.production', 'Production Order', related='quality_check_id.production_id', 
                                        store=True, depends=['quality_check_id', 'quality_check_id.production_id'])
    product_id = fields.Many2one('product.product', 'Product', related='production_id.product_id', 
                                        store=True, depends=['production_id', 'production_id.product_id'])
    
    lot_id = fields.Many2one('stock.lot', 'Lot', related='production_id.lot_producing_id', 
                                        store=True, depends=['production_id', 'production_id.lot_producing_id'])

    date = fields.Datetime('Date', related='quality_check_id.control_date', store=True, depends=['quality_check_id', 'quality_check_id.control_date'])
    weekly_signature_date = fields.Datetime('Weekly Signature Date', compute='_compute_weekly_signature_date', store=True)

    def action_view_linked_production(self):
        self.ensure_one()
        action = {
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_id': self.production_id.id,
        }
        return action

    @api.depends("signature")
    def _compute_weekly_signature_date(self):
        for rec in self:
            rec.weekly_signature_date = datetime.now()

    def action_sign_log(self):
        for rec in self:
            if not rec.signature:
                rec.signature = rec.env.user.sign_initials

    # TODO: Refactor action_view_log_lines into mixin to reduce maintenance
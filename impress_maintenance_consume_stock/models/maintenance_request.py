# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    scrap_ids = fields.One2many(comodel_name='stock.scrap', inverse_name='maintenance_request_id', string='Scraps')
    scrap_count = fields.Integer(compute='_compute_scrap_count', string='Scrap Count', store=True)
    all_scraps_done = fields.Boolean(compute='_compute_all_scraps_done', string='All Scraps Done', store=True)

    @api.depends('scrap_ids')
    def _compute_scrap_count(self):
        for record in self:
            record.scrap_count = len(record.scrap_ids)

    def _consume_parts(self):
        for record in self:
            for scrap_move in record.scrap_ids:
                if scrap_move.state != 'done':
                    scrap_move.do_scrap()

    @api.depends('scrap_ids.state', 'scrap_count')
    def _compute_all_scraps_done(self):
        for record in self:
            record.all_scraps_done = all(scrap.state == 'done' for scrap in record.scrap_ids)

    def action_consume_parts(self):
        for record in self:
            record._consume_parts()

    def action_see_move_scrap(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_stock_scrap")
        action['domain'] = [('maintenance_request_id', '=', self.id)]
        action['context'] = dict(self._context, default_origin=self.name)
        return action
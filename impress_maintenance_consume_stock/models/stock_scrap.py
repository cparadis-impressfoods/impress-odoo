# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    maintenance_request_id = fields.Many2one(comodel_name='maintenance.request', string='Maintenance Request')
    maintenance_equipement_id = fields.Many2one(related='maintenance_request_id.equipment_id', string='Equipment', store=True)

    def action_see_maintenance_id(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("impress_maintenance_consume_stock.action_open_maintenance_requests")
        action['domain'] = [('scrap_ids', 'ilike', self.id)]
        action['context'] = dict(self._context, default_origin=self.name)
        return action
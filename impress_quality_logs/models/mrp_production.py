# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    hpp_log_ids = fields.One2many('hpp.log', 'production_id', string='HPP Logs')
    loma_log_ids = fields.One2many('loma.log', 'production_id', string='LOMA Logs')
    metal_log_ids = fields.One2many('metal.log', 'production_id', string='Metal Logs')
    coding_log_ids = fields.One2many('coding.log', 'production_id', string='Coding Logs')

    def action_view_hpp_log(self):
        self.ensure_one()
        action = {
            'res_model': 'hpp.log',
            'type': 'ir.actions.act_window',
        }

        if len(self.hpp_log_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.hpp_log_ids.id
            })            # type: ignore

        else:
            action.update({
                'name': _("HPP Logs for %s", self.name),
                'domain': [('id', 'in', self.hpp_log_ids.ids)],
                'view_mode': 'tree,form',
            })             # type: ignore


        return action

    def action_view_metal_log(self):
        self.ensure_one()
        action = {
            'res_model': 'metal.log',
            'type': 'ir.actions.act_window',
        }

        if len(self.metal_log_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.metal_log_ids.id
            })            # type: ignore

        else:
            action.update({
                'name': _("Metal Logs for %s", self.name),
                'domain': [('id', 'in', self.metal_log_ids.ids)],
                'view_mode': 'tree,form',
            })             # type: ignore

        return action

    def action_view_loma_log(self):
        self.ensure_one()
        action = {
            'res_model': 'loma.log',
            'type': 'ir.actions.act_window',
        }

        if len(self.loma_log_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.loma_log_ids.id
            })            # type: ignore

        else:
            action.update({
                'name': _("LOMA Logs for %s", self.name),
                'domain': [('id', 'in', self.loma_log_ids.ids)],
                'view_mode': 'tree,form',
            })             # type: ignore

        return action
        
    def action_view_coding_log(self):
        self.ensure_one()
        action = {
            'res_model': 'coding.log',
            'type': 'ir.actions.act_window',
        }

        if len(self.coding_log_ids) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': self.coding_log_ids.id
            })            # type: ignore

        else:
            action.update({
                'name': _("LOMA Logs for %s", self.name),
                'domain': [('id', 'in', self.coding_log_ids.ids)],
                'view_mode': 'tree,form',
            })             # type: ignore

        return action
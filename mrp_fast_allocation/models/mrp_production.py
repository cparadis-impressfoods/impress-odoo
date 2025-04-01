# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def action_assign_all(self):
        for record in self:
            reception_report = record.env["report.stock.report_reception"].with_context(
                default_production_ids=[record.id]
            )
            lines = reception_report.get_report_data([record.id], None)[
                "sources_to_lines"
            ]
            for line in lines.values():
                line = line[0]
                move_out = [move.id for move in line["move_out"]]
                quantity = [line["quantity"]]
                move_ins = line["move_ins"]

                reception_report.action_assign(move_out, quantity, move_ins)

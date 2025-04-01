# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class LOMALogLine(models.Model):
    _name = "loma.log.line"
    _inherit = "log_line.mixin"
    _description = "Loma_log_line"
    _rec_name = "sequence"

    _sql_constraints = [
        (
            "unique_sequence_number",
            "UNIQUE(sequence)",
            "Sequence Number must be unique!",
        ),
    ]

    sequence = fields.Char("Sequence", default=lambda self: _("New"), copy=False)
    loma_log_id = fields.Many2one(
        comodel_name="loma.log", compute="_compute_loma_log_id", store=True
    )

    lower_limit = fields.Float(
        "Lower Limit",
        related="loma_log_id.lower_limit",
        store=True,
        depends=["loma_log_id.lower_limit"],
    )
    upper_limit = fields.Float(
        "Upper Limit",
        related="loma_log_id.upper_limit",
        store=True,
        depends=["loma_log_id.upper_limit"],
    )
    nominal_weight = fields.Float(
        "Nominal Weight",
        related="loma_log_id.nominal_weight",
        store=True,
        depends=["loma_log_id.nominal_weight"],
    )

    measure_1 = fields.Float("Measure 1")
    measure_2 = fields.Float("Measure 2")
    measure_3 = fields.Float("Measure 3")
    measure_4 = fields.Float("Measure 4")
    measure_5 = fields.Float("Measure 5")

    is_seal_ok = fields.Boolean("Seal Ok")
    is_weight_ok = fields.Boolean("Weight Ok")

    @api.depends("quality_check_id")
    def _compute_loma_log_id(self):
        for record in self:
            # Get the current worksheet field
            ws = record.active_worksheet_field
            if ws:
                record.loma_log_id = record[ws].x_loma_log_id
            else:
                record.loma_log_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "sequence" not in vals or vals["sequence"] == _("New"):
                vals["sequence"] = self.env["ir.sequence"].next_by_code(
                    "loma_log_line"
                ) or _("New")
        return super().create(vals_list)

    def action_view_log(self):
        self.ensure_one()
        action = {
            "res_model": "loma.log",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_id": self.loma_log_id.id,
        }
        return action

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CodingLog(models.Model):
    _inherit = "log.mixin"
    _name = "coding.log"
    _description = "Coding Log"

    shelf_life = fields.Integer(related="product_id.expiration_time")
    case_code = fields.Char()
    unit_code = fields.Char()

    notes = fields.Char()
    start_date = fields.Datetime()

    unit_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")])
    sleeve_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")])
    case_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")])
    subunit_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")])
    shelf_life_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")])
    keep_cold_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")])

    global_success_check = fields.Selection(
        [("ok", "Ok"), ("not_ok", "Not Ok")],
        store=True,
        compute="_compute_global_success_check",
    )

    @api.depends(
        "unit_check",
        "sleeve_check",
        "case_check",
        "subunit_check",
        "shelf_life_check",
        "keep_cold_check",
    )
    def _compute_global_success_check(self):
        for rec in self:
            if rec._check_global_success():
                rec.global_success_check = "ok"
            else:
                rec.global_success_check = "not_ok"

    def _check_global_success(self):
        self.ensure_one()
        return (
            self.unit_check == "ok"
            and self.sleeve_check == "ok"
            and self.case_check == "ok"
            and self.subunit_check == "ok"
            and self.shelf_life_check == "ok"
            and self.keep_cold_check == "ok"
        )

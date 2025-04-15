import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CodingLog(models.Model):
    _inherit = "log.mixin"
    _name = "coding.log"
    _description = "Coding Log"

    shelf_life = fields.Integer("Shelf Life", related="product_id.expiration_time")
    case_code = fields.Char("Case Code")
    unit_code = fields.Char("Unit Code")

    notes = fields.Char("Notes")
    start_date = fields.Datetime("Start Date")

    unit_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")], "Unit Check")
    sleeve_check = fields.Selection(
        [("ok", "Ok"), ("not_ok", "Not Ok")], "Sleeve Check"
    )
    case_check = fields.Selection([("ok", "Ok"), ("not_ok", "Not Ok")], "Case Check")
    subunit_check = fields.Selection(
        [("ok", "Ok"), ("not_ok", "Not Ok")], "Subunit Check"
    )
    shelf_life_check = fields.Selection(
        [("ok", "Ok"), ("not_ok", "Not Ok")], "Shelf Life Check"
    )
    keep_cold_check = fields.Selection(
        [("ok", "Ok"), ("not_ok", "Not Ok")], "Keep Cold Check"
    )

    global_success_check = fields.Selection(
        [("ok", "Ok"), ("not_ok", "Not Ok")],
        "Global Success Check",
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

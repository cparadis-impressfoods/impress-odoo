from odoo import fields, models


class CleaningMixin(models.AbstractModel):
    _name = "cleaning.mixin"
    _description = "Cleaned Item"

    cleaning_team_id = fields.Many2one("maintenance.team")
    cleaning_user_id = fields.Many2one("res.users", string="Cleaning Responsible")
    cleaning_time = fields.Float()

from odoo import models, fields, _

class CleaningMixin(models.AbstractModel):
    _name = "cleaning.mixin"
    _description = 'Cleaned Item'

    cleaning_team_id =  fields.Many2one('maintenance.team', string='Cleaning Team')
    cleaning_user_id = fields.Many2one('res.users', string='Cleaning Responsible')
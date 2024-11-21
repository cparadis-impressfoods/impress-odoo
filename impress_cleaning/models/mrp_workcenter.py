from odoo import models, fields

class MrpWorkcenter(models.Model):
    _name = 'mrp.workcenter'
    _inherit = ["mrp.workcenter", 'cleaning.mixin']


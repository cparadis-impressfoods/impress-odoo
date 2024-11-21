from odoo import models, fields

class MaintenanceEquipment(models.Model):
    _name = "maintenance.equipment"
    _inherit = ['maintenance.equipment', 'cleaning.mixin']
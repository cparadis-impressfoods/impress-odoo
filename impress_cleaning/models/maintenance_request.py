from odoo import models, fields

class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"
    _name = 'maintenance.request'
    
    maintenance_type = fields.Selection(selection_add=[('cleaning', 'Cleaning')], string='Maintenance Type', default="corrective")

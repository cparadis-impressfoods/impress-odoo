# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class MaintenanceEquipmentCategory(models.Model):
    _name = "maintenance.equipment.category"
    _inherit = ["maintenance.equipment.category", "maintenance.quality.mixin"]

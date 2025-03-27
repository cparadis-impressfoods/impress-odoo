# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    equipment_id = fields.Many2one("maintenance.equipment", string="Equipment", compute="_compute_equipment_id", search="_search_equipment_id" )
    

    @api.depends('res_model', 'res_id')
    def _compute_equipment_id(self):
        for record in self:
            if record.res_model == "maintenance.equipment":
                record.equipment_id = self.env['maintenance.equipment'].browse(record.res_id)
            else:
                record.equipment_id = False

    @api.model
    def _search_equipment_id(self, operator, value):
        # TODO: Figure out documents_project.documents_document _search_project_id() to reimplement
        if operator in ('=', '!=') and isinstance(value, bool): # needs to be the first condition as True and False are instances of int
            if not value:
                operator = operator == "=" and "!=" or "="
            return [("res_model", operator, "maintenance.equipment")]
        
        elif operator in ('=', '!=', "in", "not in") and (isinstance(value, int) or isinstance(value, list)):
            return [("res_model", "=", "maintenance.equipment"), ("res_id", operator, value),]
        else:
            raise ValidationError(_("Invalid equipment search"))
# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    maintenance_open_count_preventive = fields.Integer(
        string="Current Preventive", compute="_compute_maintenance_count_preventive"
    )
    maintenance_open_count_corrective = fields.Integer(
        string="Current Corrective", compute="_compute_maintenance_count_corrective"
    )
    document_count = fields.Integer("Document Count", compute="_compute_document_count")

    @api.depends("maintenance_count")
    def _compute_maintenance_count_preventive(self):
        for record in self:
            record.maintenance_open_count_preventive = len(
                record.maintenance_ids.filtered(
                    lambda mr: not mr.stage_id.done
                    and not mr.archive
                    and mr.maintenance_type == "preventive"
                )
            )

    @api.depends("maintenance_count")
    def _compute_maintenance_count_corrective(self):
        for record in self:
            record.maintenance_open_count_corrective = len(
                record.maintenance_ids.filtered(
                    lambda mr: not mr.stage_id.done
                    and not mr.archive
                    and mr.maintenance_type == "corrective"
                )
            )

    def _compute_document_count(self):
        Document = self.env["documents.document"]
        equipment_document_read_group = Document._read_group(
            [("res_model", "=", "maintenance.equipment"), ("res_id", "in", self.ids)],
            ["res_id"],
            ["__count"],
        )
        document_count_per_equipment_id = dict(equipment_document_read_group)
        for record in self:
            record.document_count = document_count_per_equipment_id.get(record.id, 0)

    def action_see_documents(self):
        self.ensure_one()
        return {
            "name": _("Documents"),
            "domain": [("equipment_id", "=", self.id)],
            "res_model": "documents.document",
            "type": "ir.actions.act_window",
            "views": [(False, "kanban")],
            "view_mode": "kanban",
            "context": {
                # "default_equipment_id": self.id,
                # 'default_res_model': 'maintenance.equipment',
                # 'default_res_id': self.id,
                "searchpanel_default_folder_id": self.env.ref(
                    "impress_maintenance.documents_maintenance_folder"
                ).id,
            },
        }

    def action_get_requests(self):
        self.ensure_one()
        return {
            "res_model": "maintenance.request",
            "type": "ir.actions.act_window",
            "view_mode": "kanban,form",
            "name": "Maintenance Requests",
            "domain": [("id", "in", self.maintenance_ids.ids)],
        }

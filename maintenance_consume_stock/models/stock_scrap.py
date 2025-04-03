# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class StockScrap(models.Model):
    _inherit = "stock.scrap"

    maintenance_request_id = fields.Many2one(
        comodel_name="maintenance.request",
        string="Maintenance Request",
        ondelete="cascade",
    )
    maintenance_equipement_id = fields.Many2one(
        related="maintenance_request_id.equipment_id", string="Equipment", store=True
    )

    def unlink(self):
        if self.maintenance_request_id and self.state == "done":
            raise UserError(
                "Cannot unlink a scrap move that is done and assigned to a maintenance request"
            )
        super(StockScrap, self).unlink()

    def action_see_maintenance_id(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id(
            "maintenance_consume_stock.action_open_maintenance_requests"
        )
        action["domain"] = [("scrap_ids", "ilike", self.id)]
        action["context"] = dict(self._context, default_origin=self.name)
        return action

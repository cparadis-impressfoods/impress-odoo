# -*- coding: utf-8 -*-
import logging

from odoo import models
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def record_production(self):
        if not self:
            return True
        self.pre_record_production()

        backorder = False
        if not self.env.context.get("skip_backorder"):
            # Trigger the backorder process if we produce less than expected
            if (
                float_compare(
                    self.qty_producing,  # type: ignore
                    self.qty_remaining,  # type: ignore
                    precision_rounding=self.product_uom_id.rounding,  # type: ignore
                )
                == -1
                and self.is_first_started_wo
            ):
                backorder = self.production_id._split_productions()[1:]
                for workorder in backorder.workorder_ids:
                    if workorder.product_tracking == "serial":
                        workorder.qty_producing = 1
                    elif not self.env.context.get("no_start_next", False):
                        workorder.qty_producing = workorder.qty_remaining
                self.production_id.product_qty = self.qty_producing
            else:
                if self.operation_id:
                    backorder = (
                        self.production_id.procurement_group_id.mrp_production_ids
                        - self.production_id
                    ).filtered(
                        lambda p: p.workorder_ids.filtered(
                            lambda wo: wo.operation_id == self.operation_id
                        ).state
                        not in ("cancel", "done")
                    )[
                        :1
                    ]
                else:
                    index = list(self.production_id.workorder_ids).index(self)
                    backorder = (
                        self.production_id.procurement_group_id.mrp_production_ids
                        - self.production_id
                    ).filtered(
                        lambda p: index < len(p.workorder_ids)
                        and p.workorder_ids[index].state not in ("cancel", "done")
                    )[
                        :1
                    ]

        self.move_raw_ids.picked = True
        self.production_id.move_byproduct_ids.filtered(
            lambda m: m.operation_id == self.operation_id
        ).picked = True
        self.button_finish()

        if backorder:
            for wo in (self.production_id | backorder).workorder_ids:
                if wo.state in ("done", "cancel"):
                    continue
                if (
                    not wo.current_quality_check_id
                    or not wo.current_quality_check_id.move_line_id
                ):
                    wo.current_quality_check_id.update(
                        wo._defaults_from_move(wo.move_id)
                    )
                if wo.move_id:
                    wo.current_quality_check_id._update_component_quantity()
            if not self.env.context.get("no_start_next"):
                next_wo = self.env["mrp.workorder"]
                if self.operation_id:
                    next_wo = backorder.workorder_ids.filtered(
                        lambda wo: wo.operation_id == self.operation_id
                        and wo.state in ("ready", "progress")
                    )
                else:
                    index = list(self.production_id.workorder_ids).index(self)
                    if backorder.workorder_ids[index].state in ("ready", "progress"):
                        next_wo = backorder.workorder_ids[index]
                if next_wo:
                    action = next_wo.open_tablet_view()
                    if self.employee_id:
                        action["context"]["employee_id"] = self.employee_id.id
                    return action
        return self.action_back()

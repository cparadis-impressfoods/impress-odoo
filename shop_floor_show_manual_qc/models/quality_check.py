# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class QualityCheck(models.Model):
    _inherit = 'quality.check'


    def _insert_into_wo(self):
        matching_wo = self.production_id.workorder_ids.filtered(lambda wo: wo.operation_id == self.operation_id)[0]
        self.workorder_id = matching_wo      

    def _handle_insert_into_chain(self):
        last_check = self.workorder_id.check_ids.filtered(lambda check: check != self).filtered(lambda check: not check.next_check_id)[0]
        self._insert_in_chain('after', last_check)

    def _remove_from_chain(self):
        current_previous_check = self.previous_check_id
        current_next_check = self.next_check_id
        if current_previous_check and current_next_check:
            current_previous_check.next_check_id = current_next_check
            current_next_check.previous_check_id = current_previous_check
        elif current_previous_check:
            current_previous_check.next_check_id = None
        elif current_next_check:
            current_next_check.previous_check_id = None

    def _handle_removal(self):
        self._remove_from_chain()
        vals = {}
        vals['workorder_id'] = False
        vals['previous_check_id'] = False
        vals['next_check_id'] = False  
        return vals     


    
    def write(self, vals):

        # If we're unlinking the quality check from the production or changing the production linked, we need to remove it from the chain.
        if 'production_id' in vals and vals['production_id'] != self.production_id.id:
            vals.update(self._handle_removal())

        res = super().write(vals)

        #If we just changed the production_id, we need to update the workorder_id
        if 'production_id' in vals:
            if not self.production_id:
                self.workorder_id = False
            else:
                self._insert_into_wo()
                if self.workorder_id:
                    self._handle_insert_into_chain()
        
        # If we're creating a new QC check, previous logic will not work. Here, we force a check with some recursion guards
        if not( 'next_check_id' in vals or 'previous_check_id' in vals):
            for record in self:
                record._check_if_chain_linking_needed()

        return res

    def _check_if_chain_linking_needed(self):
        self.ensure_one()
        if self.product_id and self.workorder_id:
            if not self.previous_check_id and not self.next_check_id:
                self._handle_insert_into_chain()
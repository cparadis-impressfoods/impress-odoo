# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    billback_invoice_ids = fields.Many2many('account.move', compute='_compute_billback_invoice_ids')
    billback_invoice_count = fields.Integer(compute='_compute_billback_invoice_ids')

    def _compute_billback_invoice_ids(self):
        self.billback_invoice_ids = self.invoice_ids.filtered(lambda inv: inv.billback_invoice_id).mapped(lambda inv: inv.billback_invoice_id.id)
        self.billback_invoice_count = len(self.billback_invoice_ids)

    def action_view_billback_invoice(self, invoices=False):
        """This function returns an action that display existing billback bills of
        given purchase order ids. When only one found, show the billback bill
        immediately.
        """
        if not invoices:
            self.invalidate_model(['billback_invoice_ids'])
            invoices = self.billback_invoice_ids

        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
        # choose the view_mode accordingly
        if len(invoices) > 1:
            result['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}

        return result
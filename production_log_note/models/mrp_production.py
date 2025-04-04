# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, _


_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    log_note = fields.Text(string="Log Note")

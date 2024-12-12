# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.workorder'

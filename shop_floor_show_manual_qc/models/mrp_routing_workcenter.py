# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    activity_date_deadline = fields.Datetime(
        string = 'Siguiente plato de actividad'
    )
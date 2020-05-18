# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    next_activity_date_deadline = fields.Date(
        string='Fecha siguiente actividad'
    )
    next_activity_summary = fields.Char(
        string='Resumen siguiente actividad'
    )
    next_activity_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Tipo siguiente actividad'
    )
    next_activity_activity_objective_id = fields.Many2one(
        comodel_name='mail.activity.objective',
        string='Objetivo siguiente actividad'
    )
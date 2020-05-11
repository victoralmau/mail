# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    mail_activity_objective_id = fields.Many2one(
        comodel_name='mail.activity.objective',
        string='Objetivo de actividad'
    )    
    duration = fields.Float(
        string='Duracion'
    )                
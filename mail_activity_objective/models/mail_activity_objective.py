# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MailActivityObjective(models.Model):
    _name = 'mail.activity.objective'
    _description = 'Mail Activity Objetice'
    _order = "probability desc"
    
    name = fields.Char(
        string='Nombre',
    )
    res_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Modelo'
    )
    objective_type = fields.Selection(
        selection=[
            ('reserved','Reservado'), 
            ('prospecting','Prospeccion'), 
            ('activation','Activacion'), 
            ('review','Repaso'), 
            ('closing','Cierre'), 
            ('tracking','Seguimiento'), 
            ('wake','Despertar')
        ],
        string='Tipo'
    )
    probability = fields.Integer(
        string='Probabilidad', 
        default=0
    )
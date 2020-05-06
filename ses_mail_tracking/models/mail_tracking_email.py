# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class MailTrackingEmail(models.Model):
    _inherit = 'mail.tracking.email'
    
    ses_mail_tracking_id = fields.Many2one(
        comodel_name='ses.mail.tracking',
        string='SES Mail Tracking ID'
    )
    ses_state = fields.Selection(
        selection=[
            ('none','Ninguno'), 
            ('delivery','Entregado'), 
            ('bounce','Rebote'),
            ('complaint','Reclamacion')                         
        ],
        default='none',
        string='SES Estado', 
    )
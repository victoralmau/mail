# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

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
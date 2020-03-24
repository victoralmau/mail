# -*- coding: utf-8 -*-
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'

    body = fields.Html('Contents', default='', sanitize_style=False, strip_classes=True)
    duration = fields.Float(help='Duracion en minutos y segundos')
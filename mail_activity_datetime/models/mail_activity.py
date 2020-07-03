# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    date_deadline = fields.Datetime(
        string = 'Fecha vencimiento'
    )
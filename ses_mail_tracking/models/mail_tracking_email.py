# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MailTrackingEmail(models.Model):
    _inherit = 'mail.tracking.email'
    
    ses_mail_tracking_id = fields.Many2one(
        comodel_name='ses.mail.tracking',
        string='SES Mail Tracking ID'
    )
    ses_state = fields.Selection(
        selection=[
            ('none', 'None'),
            ('delivery', 'Delivery'),
            ('bounce', 'Bounce'),
            ('complaint', 'Complaint')
        ],
        default='none',
        string='SES State',
    )

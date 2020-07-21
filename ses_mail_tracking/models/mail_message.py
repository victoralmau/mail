# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class MailMessage(models.Model):
    _inherit = 'mail.message'
    
    @api.one
    def aws_action_mail_delivery(self, message_body):
        # vals
        vals = {
            'mail_message_id': self.id,
            'message_id': message_body['mail']['messageId'],
            'date': message_body['delivery']['timestamp'],
            'response': message_body['delivery']['smtpResponse'],
            'state': 'delivery',                                                              
        }
        # check_if_exist
        ses_mail_tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', vals['mail_message_id']),
                ('message_id', '=', vals['message_id']),
                ('date', '=', vals['date']),
                ('response', '=', vals['response']),
                ('state', '=', vals['state'])
            ]
        )
        if len(ses_mail_tracking_ids) == 0:
            # create_object
            ses_mail_tracking_obj = self.env['ses.mail.tracking'].sudo().create(vals)
            # recipients
            if "recipients" in message_body['delivery']:
                for recipient in message_body['delivery']['recipients']:
                    vals = {
                        'ses_mail_tracking_id': ses_mail_tracking_obj.id,
                        'recipient': recipient                                                              
                    }
                    self.env['ses.mail.tracking.recipient'].sudo().create(vals)
            # mail_tracking_email
            mail_tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                [
                    ('mail_message_id', '=', self.id)
                ]
            )
            if mail_tracking_email_ids:
                for mail_tracking_email_id in mail_tracking_email_ids:
                    mail_tracking_email_id.ses_mail_tracking_id =  ses_mail_tracking_obj.id                                
            # recipients
            if "recipients" in message_body['delivery']:
                if mail_tracking_email_ids:
                    for recipient in message_body['delivery']['recipients']:
                        for mail_tracking_email_id in mail_tracking_email_ids:                                                
                            if recipient in mail_tracking_email_id.recipient:
                                mail_tracking_email_id.state = 'delivered'
                                mail_tracking_email_id.ses_state = ses_mail_tracking_obj.state
                                
    @api.one
    def aws_action_mail_bounce(self, message_body):
        vals = {
            'mail_message_id': self.id,
            'message_id': message_body['mail']['messageId'],
            'date': message_body['bounce']['timestamp'],
            'response': str(message_body['bounce']['bounceType'])+' - '+str(message_body['bounce']['bounceSubType']),
            'state': 'bounce',                                                              
        }
        # check_if_exist
        ses_mail_tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', vals['mail_message_id']),
                ('message_id', '=', vals['message_id']),
                ('date', '=', vals['date']),
                ('response', '=', vals['response']),
                ('state', '=', vals['state'])
            ]
        )
        if len(ses_mail_tracking_ids) == 0:
            # create_object
            ses_mail_tracking_obj = self.env['ses.mail.tracking'].sudo().create(vals)
            # recipients
            if "bouncedRecipients" in message_body['bounce']:
                for bounced_recipient in message_body['bounce']['bouncedRecipients']:
                    vals = {
                        'ses_mail_tracking_id': ses_mail_tracking_obj.id,
                        'recipient': bounced_recipient['emailAddress']                                                              
                    }
                    self.env['ses.mail.tracking.recipient'].sudo().create(vals)
            # mail_tracking_email
            mail_tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                [
                    ('mail_message_id', '=', self.id)
                ]
            )
            if mail_tracking_email_ids:
                for mail_tracking_email_id in mail_tracking_email_ids:
                    mail_tracking_email_id.ses_mail_tracking_id = ses_mail_tracking_obj.id
            # bouncedRecipients
            if "bouncedRecipients" in message_body['bounce']:
                mail_tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                    [
                        ('mail_message_id', '=', self.id)
                    ]
                )
                if mail_tracking_email_ids:
                    for bounced_recipient in message_body['bounce']['bouncedRecipients']:
                        for mail_tracking_email_id in mail_tracking_email_ids:
                            if bounced_recipient['emailAddress'] in mail_tracking_email_id.recipient:
                                # prevent_errors if previously delivery
                                if mail_tracking_email_id.ses_state != 'delivery':
                                    mail_tracking_email_id.state = 'bounced'
                                    mail_tracking_email_id.ses_state = ses_mail_tracking_obj.state
                                    
    @api.one
    def aws_action_mail_complaint(self, message_body):
        vals = {
            'mail_message_id': self.id,
            'message_id': message_body['mail']['messageId'],
            'date': message_body['complaint']['timestamp'],
            'response': '',
            'state': 'complaint',                                                              
        }
        # complaintFeedbackType
        if "complaintFeedbackType" in message_body['complaint']:
             vals['response'] = message_body['complaint']['complaintFeedbackType']
        # check_if_exist
        ses_mail_tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', vals['mail_message_id']),
                ('message_id', '=', vals['message_id']),
                ('date', '=', vals['date']),
                ('response', '=', vals['response']),
                ('state', '=', vals['state'])
            ]
        )
        if len(ses_mail_tracking_ids) == 0:
            # create_object
            ses_mail_tracking_obj = self.env['ses.mail.tracking'].sudo().create(vals)
            # recipients
            if "complainedRecipients" in message_body['complaint']:
                for complaint_recipient in message_body['complaint']['complainedRecipients']:
                    vals = {
                        'ses_mail_tracking_id': ses_mail_tracking_obj.id,
                        'recipient': complaint_recipient['emailAddress']                                                              
                    }
                    self.env['ses.mail.tracking.recipient'].sudo().create(vals)
            # mail_tracking_email
            mail_tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                [
                    ('mail_message_id', '=', self.id)
                ]
            )
            if mail_tracking_email_ids:
                for mail_tracking_email_id in mail_tracking_email_ids:
                    mail_tracking_email_id.ses_mail_tracking_id = ses_mail_tracking_obj.id
            # complainedRecipients
            if "complainedRecipients" in message_body['complaint']:
                mail_tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                    [
                        ('mail_message_id', '=', self.id)
                    ]
                )
                if mail_tracking_email_ids:
                    for complaint_recipient in message_body['complaint']['complainedRecipients']:
                        for mail_tracking_email_id in mail_tracking_email_ids:
                            if complaint_recipient['emailAddress'] in mail_tracking_email_id.recipient:
                                # prevent_errors if previously delivery
                                if mail_tracking_email_id.ses_state != 'delivery':
                                    mail_tracking_email_id.state = 'bounced'
                                    mail_tracking_email_id.ses_state = ses_mail_tracking_obj.state
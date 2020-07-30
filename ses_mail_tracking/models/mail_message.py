# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models

class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.multi
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
        tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', vals['mail_message_id']),
                ('message_id', '=', vals['message_id']),
                ('date', '=', vals['date']),
                ('response', '=', vals['response']),
                ('state', '=', vals['state'])
            ]
        )
        if len(tracking_ids) == 0:
            # create_object
            tracking_obj = self.env['ses.mail.tracking'].sudo().create(vals)
            # recipients
            if "recipients" in message_body['delivery']:
                for recipient in message_body['delivery']['recipients']:
                    vals = {
                        'ses_mail_tracking_id': tracking_obj.id,
                        'recipient': recipient                                                              
                    }
                    self.env['ses.mail.tracking.recipient'].sudo().create(vals)
            # mail_tracking_email
            tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                [
                    ('mail_message_id', '=', self.id)
                ]
            )
            if tracking_email_ids:
                for tracking_email_id in tracking_email_ids:
                    tracking_email_id.ses_mail_tracking_id = tracking_obj.id
            # recipients
            if "recipients" in message_body['delivery']:
                if tracking_email_ids:
                    for recipient in message_body['delivery']['recipients']:
                        for tracking_email_id in tracking_email_ids:
                            if recipient in tracking_email_id.recipient:
                                tracking_email_id.state = 'delivered'
                                tracking_email_id.ses_state = tracking_obj.state
                                
    @api.multi
    def aws_action_mail_bounce(self, message_body):
        vals = {
            'mail_message_id': self.id,
            'message_id': message_body['mail']['messageId'],
            'date': message_body['bounce']['timestamp'],
            'response': '%s - %s' % (
                str(message_body['bounce']['bounceType']),
                str(message_body['bounce']['bounceSubType'])
            ),
            'state': 'bounce',                                                              
        }
        # check_if_exist
        tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', vals['mail_message_id']),
                ('message_id', '=', vals['message_id']),
                ('date', '=', vals['date']),
                ('response', '=', vals['response']),
                ('state', '=', vals['state'])
            ]
        )
        if len(tracking_ids) == 0:
            # create_object
            tracking_obj = self.env['ses.mail.tracking'].sudo().create(vals)
            # recipients
            if "bouncedRecipients" in message_body['bounce']:
                for bounced_recipient in message_body['bounce']['bouncedRecipients']:
                    vals = {
                        'ses_mail_tracking_id': tracking_obj.id,
                        'recipient': bounced_recipient['emailAddress']                                                              
                    }
                    self.env['ses.mail.tracking.recipient'].sudo().create(vals)
            # mail_tracking_email
            tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                [
                    ('mail_message_id', '=', self.id)
                ]
            )
            if tracking_email_ids:
                for tracking_email_id in tracking_email_ids:
                    tracking_email_id.ses_mail_tracking_id = tracking_obj.id
            # bouncedRecipients
            if "bouncedRecipients" in message_body['bounce']:
                tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                    [
                        ('mail_message_id', '=', self.id)
                    ]
                )
                if tracking_email_ids:
                    for bounced_recipient in message_body['bounce']['bouncedRecipients']:
                        for tracking_email_id in tracking_email_ids:
                            if bounced_recipient['emailAddress'] in tracking_email_id.recipient:
                                # prevent_errors if previously delivery
                                if tracking_email_id.ses_state != 'delivery':
                                    tracking_email_id.state = 'bounced'
                                    tracking_email_id.ses_state = tracking_obj.state
                                    
    @api.multi
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
        mail_tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', vals['mail_message_id']),
                ('message_id', '=', vals['message_id']),
                ('date', '=', vals['date']),
                ('response', '=', vals['response']),
                ('state', '=', vals['state'])
            ]
        )
        if len(mail_tracking_ids) == 0:
            # create_object
            tracking_obj = self.env['ses.mail.tracking'].sudo().create(vals)
            # recipients
            if "complainedRecipients" in message_body['complaint']:
                for complaint_recipient in message_body['complaint']['complainedRecipients']:
                    vals = {
                        'ses_mail_tracking_id': tracking_obj.id,
                        'recipient': complaint_recipient['emailAddress']                                                              
                    }
                    self.env['ses.mail.tracking.recipient'].sudo().create(vals)
            # mail_tracking_email
            tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                [
                    ('mail_message_id', '=', self.id)
                ]
            )
            if tracking_email_ids:
                for tracking_email_id in tracking_email_ids:
                    tracking_email_id.ses_mail_tracking_id = tracking_obj.id
            # complainedRecipients
            if "complainedRecipients" in message_body['complaint']:
                tracking_email_ids = self.env['mail.tracking.email'].sudo().search(
                    [
                        ('mail_message_id', '=', self.id)
                    ]
                )
                if tracking_email_ids:
                    for complaint_recipient in message_body['complaint']['complainedRecipients']:
                        for tracking_email_id in tracking_email_ids:
                            if complaint_recipient['emailAddress'] in tracking_email_id.recipient:
                                # prevent_errors if previously delivery
                                if tracking_email_id.ses_state != 'delivery':
                                    tracking_email_id.state = 'bounced'
                                    tracking_email_id.ses_state = tracking_obj.state

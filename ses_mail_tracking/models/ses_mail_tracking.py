# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, tools

import json
import logging
_logger = logging.getLogger(__name__)

import boto3
from botocore.exceptions import ClientError

class SesMailTracking(models.Model):
    _name = 'ses.mail.tracking'
    _description = 'SES Mail Tracking'    
        
    mail_message_id = fields.Many2one(
        comodel_name='mail.message',
        string='Mail Message Id'
    )
    message_id = fields.Char(        
        string='Message Id'
    )
    date = fields.Date(        
        string='Date'
    )
    response = fields.Text(        
        string='Response'
    )
    state = fields.Selection(
        selection=[
            ('none','None'),
            ('delivery','Delivery'),
            ('bounce','Bounce'),
            ('complaint','Complaint')
        ],
        default='none',
        string='State',
    )
    recipient_ids = fields.One2many('ses.mail.tracking.recipient', 'ses_mail_tracking_id', string='Recipients')
    
    def item_exist(self, params):
        exist = False
        ses_mail_tracking_ids = self.env['ses.mail.tracking'].sudo().search(
            [
                ('mail_message_id', '=', params['mail_message_id']),
                ('message_id', '=', params['message_id']),
                ('date', '=', params['date']),
                ('response', '=', params['response']),
                ('state', '=', params['state'])
            ]
        )
        if ses_mail_tracking_ids:
            exist = True
            
        return exist        
    
    @api.model    
    def cron_check_ses_mail_tracking(self):
        ses_sqs_url = tools.config.get('ses_sqs_url')
        AWS_ACCESS_KEY_ID = tools.config.get('aws_access_key_id')        
        AWS_SECRET_ACCESS_KEY = tools.config.get('aws_secret_key_id')
        AWS_SMS_REGION_NAME = tools.config.get('aws_region_name')                        
        # boto3
        sqs = boto3.client(
            'sqs',
            region_name=AWS_SMS_REGION_NAME, 
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key= AWS_SECRET_ACCESS_KEY
        )        
        # Receive message from SQS queue
        total_messages = 10
        while total_messages>0:
            response = sqs.receive_message(
                QueueUrl=ses_sqs_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=10,
                MessageAttributeNames=['All']
            )
            if 'Messages' in response:
                total_messages = len(response['Messages'])
            else:
                total_messages = 0
            # continue
            if 'Messages' in response:
                for message in response['Messages']:                                
                    message_body = json.loads(message['Body'])   
                    if 'mail' in message_body:              
                        notification_type_lower = str(message_body['notificationType'].lower())
                        # message_id_odoo
                        message_id_odoo = False            
                        if 'headers' in message_body['mail']:
                            if len(message_body['mail']['headers']) > 0:
                                for header in message_body['mail']['headers']:                
                                    if header['name']=='Message-Id':
                                        message_id_odoo = header['value'].strip()
                                        mail_message_ids = self.env['mail.message'].sudo().search(
                                            [
                                                ('message_id', '=', message_id_odoo)
                                            ]
                                        )
                                        if mail_message_ids:
                                            for mail_message_id in mail_message_ids:
                                                # notification_type_lower
                                                if notification_type_lower == 'delivery':
                                                    mail_message_id.aws_action_mail_delivery(message_body)
                                                elif notification_type_lower == 'bounce':
                                                    mail_message_id.aws_action_mail_bounce(message_body)
                                                elif notification_type_lower == 'complaint':
                                                    mail_message_id.aws_action_mail_complaint(message_body)
                    # remove_message
                    sqs.delete_message(
                        QueueUrl=ses_sqs_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )                                        
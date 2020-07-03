# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models, fields

import logging
_logger = logging.getLogger(__name__)

class MailMail(models.Model):
    _inherit = 'mail.mail'                                
   
    @api.model    
    def cron_action_check_mails_exceptions(self): 
    
        mail_catchall = str(self.env['ir.config_parameter'].get_param('mail.catchall.alias'))+"@"+str(self.env['ir.config_parameter'].get_param('mail.catchall.domain'))        
    
        mail_mail_ids = self.env['mail.mail'].search([('state', '=', 'exception')])
        
        for mail_mail_id in mail_mail_ids:
            if "Message rejected: Email address is not verified" in mail_mail_id.failure_reason:
                email_from_split = mail_mail_id.mail_message_id.email_from.split("<")
                if len(email_from_split)>1:
                    if email_from_split[1]!=mail_catchall:
                        mail_mail_id.mail_message_id.email_from = email_from_split[0]+'<'+mail_catchall+'>'
                        
                        mail_mail_id.mark_outgoing()
                        mail_mail_id.send()
                else:
                    if '@' in mail_mail_id.mail_message_id.email_from:
                        mail_mail_id.mail_message_id.email_from = mail_catchall
                        
                        mail_mail_id.mark_outgoing()
                        mail_mail_id.send()
                    else:
                        _logger.info('Pasa algo raro con '+mail_mail_id.mail_message_id.email_from)
                        
            elif "Transaction failed: Local address contains control or whitespace" in mail_mail_id.failure_reason:
                email_from_replace = mail_mail_id.mail_message_id.email_from.replace('[', '-').replace(']', '-')
                
                mail_mail_id.mail_message_id.email_from = email_from_replace
                
                mail_mail_id.mark_outgoing()
                mail_mail_id.send()           
                
    @api.model
    def create(self, values):
        return_object = super(MailMail, self).create(values)
        #override reply_to
        if return_object.email_from!=False:
            return_object.reply_to = return_object.email_from 
        #return            
        return return_object                                                                                                           
# -*- coding: utf-8 -*-
from openerp import api, models, fields
from openerp.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'        
    
    @api.one
    def generate_auto_starred_slack(self, user_id):
        return True
        
    @api.one
    def generate_notice_message_without_auto_starred_user_slack(self):
        return True
    
    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(MailMessage, self).create(values)
        
        if record._name=="mail.message":
            starred_any_user = False
            
            if len(record.needaction_partner_ids)>0:            
                for partner_id in record.needaction_partner_ids:
                    if partner_id.id!=self.env.user.partner_id.id:
                        starred_item = False
                        for user_id in partner_id.user_ids:
                            if user_id.id>0:
                                starred_item = True
                                starred_any_user = True
                                record.generate_auto_starred_slack(user_id)#Fix slack
                                
                        if starred_item==True:
                            record.starred_partner_ids = [(4, partner_id.id)]
            else:
                if record.message_type=='email':
                    mail_followers_ids = self.env['mail.followers'].search([('res_model', '=', record.model),('res_id', '=', record.res_id)])                         
                    for mail_follower in mail_followers_ids:
                        for user_id in mail_follower.partner_id.user_ids:
                            if user_id.id>0:
                                starred_any_user = True
                                record.starred_partner_ids = [(4, mail_follower.partner_id.id)]                                
                                record.generate_auto_starred_slack(user_id)#Fix slack                        
                            
            if starred_any_user==False:
                notice_message_skip = False
                for user_id in record.author_id.user_ids:
                    if user_id.id>0: 
                        notice_message_skip = True                   
                
                if notice_message_skip==False:
                    record.generate_notice_message_without_auto_starred_user_slack()#Fix slack notice                            
                                                                                                                        
        return record                                             
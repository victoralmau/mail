# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.tools.safe_eval import safe_eval

import logging
_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'                                
                
    @api.multi
    def message_get_email_values(self, notif_mail=None):
        res = super(MailThread, self).message_get_email_values(notif_mail=notif_mail)
        
        mail_mail_headers_override_add = self.env['ir.config_parameter'].sudo().get_param('mail_mail_headers_override_add')
        if mail_mail_headers_override_add!=False:                
            if res.get('headers'):
                headers = {}
                headers.update(safe_eval(res['headers']))
                res['headers'] = repr(headers)
                headers_new = res['headers'][0:-1]+",'"+str(mail_mail_headers_override_add)+"'}"
                res['headers'] = headers_new
                                                                                                                
        return res                                                                                                                                          
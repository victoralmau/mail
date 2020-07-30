# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools.safe_eval import safe_eval


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def message_get_email_values(self, notif_mail=None):
        res = super(MailThread, self).message_get_email_values(notif_mail=notif_mail)

        override_add = self.env['ir.config_parameter'].sudo().get_param(
            'mail_mail_headers_override_add'
        )
        if override_add:
            if res.get('headers'):
                headers = {}
                headers.update(safe_eval(res['headers']))
                res['headers'] = repr(headers)
                res['headers'] = "%s,'%s'}" % (res['headers'][0:-1], override_add)

        return res

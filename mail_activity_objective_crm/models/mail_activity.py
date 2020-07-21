# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.model
    def create(self, values):
        return_object = super(MailActivity, self).create(values)
        # operations
        if return_object.res_model == 'crm.lead':
            super(MailActivity, return_object).regenerate_model_field(return_object.res_model, return_object.res_id)
        # return
        return return_object

    @api.one
    def write(self, vals):
        return_write = super(MailActivity, self).write(vals)
        # operations
        if self.res_model == 'crm.lead':
            super(MailActivity, self).regenerate_model_field(self.res_model, self.res_id)
        # return
        return return_write

    @api.multi
    def unlink(self):
        # operations
        need_regenerate_model_field = False
        res_id = 0
        for item in self:
            # override
            if item.res_model == 'crm.lead':
                need_regenerate_model_field = True
                res_id = item.res_id
        # return
        return_unlink = super(MailActivity, self).unlink()
        # operations2
        if need_regenerate_model_field:
            super(MailActivity, self).regenerate_model_field('crm.lead', res_id)
        # return
        return return_unlink
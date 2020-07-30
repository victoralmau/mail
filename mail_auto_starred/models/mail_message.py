# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.multi
    def generate_auto_starred_slack(self, user_id):
        return True

    @api.multi
    def generate_notice_message_without_auto_starred_user_slack(self):
        return True

    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(MailMessage, self).create(values)
        if record._name == "mail.message":
            starred_any_user = False
            if record.needaction_partner_ids:
                for partner_id in record.needaction_partner_ids:
                    if partner_id.id != self.env.user.partner_id.id:
                        starred_item = False
                        for user_id in partner_id.user_ids:
                            if user_id:
                                starred_item = True
                                starred_any_user = True
                                record.generate_auto_starred_slack(user_id)
                        if starred_item:
                            record.starred_partner_ids = [(4, partner_id.id)]
            else:
                if record.message_type == 'email':
                    followers_ids = self.env['mail.followers'].search(
                        [
                            ('res_model', '=', record.model),
                            ('res_id', '=', record.res_id)
                        ]
                    )
                    for followers_id in followers_ids:
                        for user_id in followers_id.partner_id.user_ids:
                            if user_id:
                                starred_any_user = True
                                record.starred_partner_ids = [
                                    (4, followers_id.partner_id.id)
                                ]
                                record.generate_auto_starred_slack(user_id)

            if not starred_any_user:
                notice_message_skip = False
                for user_id in record.author_id.user_ids:
                    if user_id:
                        notice_message_skip = True

                if not notice_message_skip:
                    record.generate_notice_message_without_auto_starred_user_slack()

        return record

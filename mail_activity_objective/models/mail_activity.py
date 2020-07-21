# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    activity_objective_id = fields.Many2one(
        comodel_name='mail.activity.objective',
        string='Activity objective'
    )    
    duration = fields.Float(
        string='Duration'
    )

    @api.one
    def get_old_item_without(self, res_model, res_id):
        return_item = {
            'date_deadline': False,
            'summary': '',
            'activity_type_id': 0,
            'activity_objective_id': 0,
        }
        mail_activity_ids = self.env['mail.activity'].sudo().search(
            [
                ('res_model', '=', res_model),
                ('res_id', '=', res_id)
            ],
            order="date_deadline asc"
        )
        if mail_activity_ids:
            mail_activity_id = mail_activity_ids[0]
            return_item = {
                'date_deadline': mail_activity_id.date_deadline,
                'summary': mail_activity_id.summary,
                'activity_type_id': mail_activity_id.activity_type_id.id,
                'activity_objective_id': mail_activity_id.activity_objective_id.id
            }
        # return
        return return_item

    @api.one
    def regenerate_model_field(self, res_model, res_id):
        old_item = self.get_old_item_without(res_model, res_id)[0]
        # res_model_item
        res_model_item = self.env[res_model].sudo().browse(res_id)
        # next_activity_date_deadline
        if 'next_activity_date_deadline' in res_model_item:
            res_model_item.next_activity_date_deadline = old_item['date_deadline']
        # next_activity_summary
        if 'next_activity_summary' in res_model_item:
            res_model_item.next_activity_summary = old_item['summary']
        # next_activity_activity_type_id
        if 'next_activity_activity_type_id' in res_model_item:
            res_model_item.next_activity_activity_type_id = old_item['activity_type_id']
        # next_activity_activity_objective_id
        if 'next_activity_activity_objective_id' in res_model_item:
            res_model_item.next_activity_activity_objective_id = old_item['activity_objective_id']
        # return
        return res_model_item
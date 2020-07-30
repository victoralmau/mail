# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    
    activity_objective_id = fields.Many2one(
        comodel_name='mail.activity.objective',
        string='Activity objective'
    )    
    duration = fields.Float(
        string='Duration'
    )

    @api.multi
    def get_old_item_without(self, res_model, res_id):
        res = {
            'date_deadline': False,
            'summary': '',
            'activity_type_id': 0,
            'activity_objective_id': 0,
        }
        activity_ids = self.env['mail.activity'].sudo().search(
            [
                ('res_model', '=', res_model),
                ('res_id', '=', res_id)
            ],
            order="date_deadline asc"
        )
        if activity_ids:
            res = {
                'date_deadline': activity_ids[0].date_deadline,
                'summary': activity_ids[0].summary,
                'activity_type_id': activity_ids[0].activity_type_id.id,
                'activity_objective_id': activity_ids[0].activity_objective_id.id
            }
        # return
        return res

    @api.multi
    def regenerate_model_field(self, res_model, res_id):
        old_item = self.get_old_item_without(res_model, res_id)[0]
        # res_model_item
        res = self.env[res_model].sudo().browse(res_id)
        # next_activity_date_deadline
        if 'next_activity_date_deadline' in res:
            res.next_activity_date_deadline = old_item['date_deadline']
        # next_activity_summary
        if 'next_activity_summary' in res:
            res.next_activity_summary = old_item['summary']
        # next_activity_activity_type_id
        if 'next_activity_activity_type_id' in res:
            res.next_activity_activity_type_id = old_item['activity_type_id']
        # next_activity_activity_objective_id
        if 'next_activity_activity_objective_id' in res:
            res.next_activity_activity_objective_id = old_item['activity_objective_id']
        # return
        return res

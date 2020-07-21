# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    next_activity_date_deadline = fields.Date(
        string='Next activity date deadline'
    )
    next_activity_summary = fields.Char(
        string='Next activity summary'
    )
    next_activity_activity_type_id = fields.Many2one(
        comodel_name='mail.activity.type',
        string='Next activity type id'
    )
    next_activity_activity_objective_id = fields.Many2one(
        comodel_name='mail.activity.objective',
        string='Next activity objective id'
    )
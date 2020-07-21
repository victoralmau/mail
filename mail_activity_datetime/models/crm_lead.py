# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    activity_date_deadline = fields.Datetime(
        string='Activity date deadline'
    )
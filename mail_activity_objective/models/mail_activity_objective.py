# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailActivityObjective(models.Model):
    _name = 'mail.activity.objective'
    _description = 'Mail Activity Objetice'
    _order = "probability desc"
    
    name = fields.Char(
        string='Name',
    )
    res_model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model'
    )
    objective_type = fields.Selection(
        selection=[
            ('reserved','Reserved'),
            ('prospecting','Prospecting'),
            ('activation','Activation'),
            ('review','Review'),
            ('closing','Closing'),
            ('tracking','Tracking'),
            ('wake','Wake')
        ],
        string='Type'
    )
    probability = fields.Integer(
        string='Probability',
        default=0
    )
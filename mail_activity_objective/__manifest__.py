# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Mail Activity Objective',
    'version': '12.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'mail', 'mail_activity_done'],
    'data': [
        'views/mail_activity_views.xml',
        'views/mail_activity_objective_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
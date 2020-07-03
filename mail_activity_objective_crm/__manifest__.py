# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Mail Activity Objective Crm',
    'version': '12.0.1.0.0',
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'mail_activity_objective', 'crm'],
    'data': [
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
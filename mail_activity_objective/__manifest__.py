# -*- coding: utf-8 -*-
{
    'name': 'Mail Activity Objective',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'crm', 'mail'],
    'data': [
        'data/ir_cron.xml',
        'views/mail_activity_views.xml',
        'views/mail_activity_objective_views.xml',
        'views/crm_lead.xml',
        'views/template.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': ['static/src/xml/buttons.xml'],
    'installable': True,
    'auto_install': False,    
}
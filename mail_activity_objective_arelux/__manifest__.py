# -*- coding: utf-8 -*-
{
    'name': 'Mail Activity Objective Arelux',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['mail_activity_objective', 'sale_arelux'],
    'data': [
        'data/ir_cron.xml',
        'views/crm_lead.xml',
    ],
    'installable': True,
    'auto_install': False,    
}
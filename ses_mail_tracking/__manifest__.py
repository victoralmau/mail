# -*- coding: utf-8 -*-
{
    'name': 'SES Mail Tracking',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'mail', 'mail_tracking'],
    'data': [
        'data/ir_cron.xml',
        'views/mail_tracking_view.xml',
        'views/ses_mail_tracking_view.xml',
        'security/ir.model.access.csv',
    ],
    'external_dependencies': {
        'python3' : ['boto3'],
    },
    'installable': True,
    'auto_install': False,    
}
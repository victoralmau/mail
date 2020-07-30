# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "SES Mail Tracking",
    "version": "12.0.1.0.0",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "website": "https://nodrizatech.com/",
    "category": "Tools",
    "license": "AGPL-3",
    "depends": [
        "base",
        "mail",
        "mail_tracking"
    ],
    "data": [
        "data/ir_cron.xml",
        "views/mail_tracking_view.xml",
        "views/ses_mail_tracking_view.xml",
        "security/ir.model.access.csv",
    ],
    "external_dependencies": {
        "python": ["boto3"],
    },
    "installable": True
}

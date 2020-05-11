# -*- coding: utf-8 -*-
from openerp import api, models, fields
from openerp.exceptions import Warning, ValidationError

import logging
_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    mail_activity_objective_id = fields.Many2one(
        comodel_name='mail.activity.objective',
        track_visibility='onchange',
        string='Objetivo de actividad'
    )        
    
    @api.model    
    def cron_odoo_crm_lead_change_empty_mail_activity_objective_id(self):
        _logger.info('cron_odoo_crm_lead_change_empty_mail_activity_objective_id')                
    
    @api.model    
    def cron_odoo_crm_lead_change_seguimiento(self):
        _logger.info('cron_odoo_crm_lead_change_seguimiento')                                                                            
    
    @api.model    
    def cron_odoo_crm_lead_change_dormidos(self):
        _logger.info('cron_odoo_crm_lead_change_dormidos')                    
                    
    @api.model    
    def action_boton_pedir_dormido(self):        
        _logger.info('action_boton_pedir_dormido')                                                                                                    
    
    @api.model    
    def cron_odoo_crm_lead_change_inactivos(self):
        _logger.info('cron_odoo_crm_lead_change_inactivos')                           
    
    @api.model                        
    def action_boton_pedir_activo(self):
        _logger.info('action_boton_pedir_activo')                                                                    
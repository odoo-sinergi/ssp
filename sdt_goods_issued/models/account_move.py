from odoo import fields, models, api, _


class AccountMoveLine(models.Model):
    _inherit='account.move.line'


    analytic_product_id = fields.Many2one('account.analytic.account', string='Analytic Product', domain="[('plan_id.name','=','Product')]")
    analytic_project_id = fields.Many2one('account.analytic.account', string='Analytic Project', domain="[('plan_id.name','=','Project')]")

    
    


    


    
    

    

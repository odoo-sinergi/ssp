from odoo import fields, models, api, _

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'


    plan_name = fields.Char(related='plan_id.name', string='Plan Name', store=True)

    




    


    


    
    

    

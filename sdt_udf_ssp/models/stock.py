from odoo import fields, models, api, _

class StockPicking(models.Model):
    _inherit='stock.picking'

    # work_base_structure = fields.Many2one('account.analytic.account', string='Work Base Structure')
    jitcall = fields.Char(string='JIT Call')


    # def button_validate(self):
    #     res = super().button_validate()
    #     for data in self:
    #         if data.work_base_structure.id:
    #             all_analytic = {}
    #             all_analytic.update({str(data.work_base_structure.id) : 100})
    #             for move in data.move_ids:
    #                 for value in move.stock_valuation_layer_ids:
    #                     for amv in value.account_move_id:
    #                         for amlv in amv.line_ids:
    #                             amlv.analytic_distribution = all_analytic
    #     return res


class StockMove(models.Model):
    _inherit='stock.move'

    

    


    


    
    

    

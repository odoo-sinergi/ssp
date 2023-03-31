from odoo import api, fields, models, _ , SUPERUSER_ID
#from odoo.addons.product.models import decimal_precision as dp
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
from lxml import etree
class AccountMove(models.Model):
    _inherit='account.move'

    picking_tt_ids = fields.Many2many(string='Stock Picking DO',comodel_name='stock.picking', relation='account_move_stock_picking_tt',column1='move_id',column2='Picking_tt_id',)
    # fields fix
    stock_picking_tt_ids = fields.Many2many(string='Delivery Order',comodel_name='stock.picking', relation='account_picking_tt_rel',column1='move_id',column2='picking_id',)
    picking_tt = fields.Boolean(string='Picking DO',)
    

    # @api.onchange('stock_picking_tt_ids','picking_tt')
    # def onchange_stock_picking_tt_ids(self):
    #     picking_obj = self.env['stock.picking'].search([('origin', '=', self.invoice_origin),('picking_type_code', '=', 'internal')])
    #     picking_list=[]
    #     for line in picking_obj:
    #         picking_list.append(line.id)
    #     domain = {'stock_picking_tt_ids': [('id', '=', picking_list)]}
    #     return {'domain': domain} 
    
    def action_post(self):
        res = super().action_post()
        for data in self:
            for stock_picking_tt_id in data.stock_picking_tt_ids :
                if stock_picking_tt_id :
                    stock_picking_tt_id.invoice_id = data.id
        return res



    
    

    

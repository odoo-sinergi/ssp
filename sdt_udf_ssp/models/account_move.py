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
    stock_picking_tt_ids = fields.Many2many(string='DO',comodel_name='stock.picking', relation='account_picking_tt_rel',column1='move_id',column2='picking_id',)
    picking_tt = fields.Boolean(string='Picking DO',)
    

    def unlink_move_line (self):
        self.invoice_line_ids.unlink()
        self.create_invoice_line()
    
    def unlink_invoice_number_picking (self):
        for stock_picking_tt_id in self.stock_picking_tt_ids :
            if stock_picking_tt_id :
                stock_picking_tt_id.invoice_id = False
        self.invoice_line_ids.sudo().unlink()
        self.stock_picking_tt_ids = False
        
    
    def action_post(self):
        res = super().action_post()
        for data in self:
            for stock_picking_tt_id in data.stock_picking_tt_ids :
                if stock_picking_tt_id :
                    stock_picking_tt_id.invoice_id = data.id
        return res

    @api.onchange('stock_picking_tt_ids')
    def onchange_stock_picking_tt_ids(self):
        for stock_picking_tt_id in self.stock_picking_tt_ids :
            if stock_picking_tt_id:
                order = stock_picking_tt_id.move_ids_without_package.sale_line_id.order_id
                partner = order.partner_invoice_id
                self.partner_id = partner.id
                self.invoice_date = stock_picking_tt_id.force_date
                self.date = stock_picking_tt_id.force_date
                self.invoice_payment_term_id = order.partner_id.property_payment_term_id
                self.ref = order.client_order_ref or ''
                
    def create_invoice_line (self):
        aml_obj = self.env["account.move.line"]
        for stock_picking_tt_id in self.stock_picking_tt_ids :
            for stock_move in stock_picking_tt_id.move_ids_without_package :
                account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
                so_line = stock_move.sale_line_id
                invoices = aml_obj.create({
                    "name": so_line.name,
                    "move_id": self.id,
                    "account_id": account,
                    "price_unit": so_line.price_unit,
                    "quantity": stock_move.quantity_done,
                    "currency_id": so_line.currency_id.id,
                    "product_uom_id": so_line.product_uom.id,
                    "product_id": so_line.product_id.id,
                    "sale_line_ids": [(6, 0, so_line.ids)],
                    "tax_ids": [(6, 0, so_line.tax_id.ids)],
                })
        self.filter_invoice_line()

    # @api.model
    def filter_invoice_line (self):
        pack = []
        total_qty = 0

        for record in self.invoice_line_ids:
            if not pack :
                total_qty = record.quantity
                total_qty = record.quantity
                pack.append((0,0,{
                    "name": record.name,
                    "move_id": record.id,
                    "account_id": record.account_id.id,
                    "price_unit": record.price_unit,
                    "quantity": record.quantity,
                    "currency_id": record.currency_id.id,
                    "product_uom_id": record.product_uom_id.id,
                    "product_id": record.product_id.id,
                    "sale_line_ids": [(4,record.sale_line_ids.id)],
                    "tax_ids": [(6, 0, record.tax_ids.ids)],
                }))
            else :
                check_data = [d for d in pack if d[2]['product_id'] == record.product_id.id]
                if not check_data :
                    total_qty = record.quantity
                    pack.append((0,0,{
                        "name": record.name,
                        "move_id": record.id,
                        "account_id": record.account_id.id,
                        "price_unit": record.price_unit,
                        "quantity": total_qty,
                        "currency_id": record.currency_id.id,
                        "product_uom_id": record.product_uom_id.id,
                        "product_id": record.product_id.id,
                        "sale_line_ids": [(4, record.sale_line_ids.id)],
                        "tax_ids": [(6, 0, record.tax_ids.ids)],
                    }))
                else :
                    qty_var = check_data[0][2]['quantity'] + record.quantity
                    for pk in pack :
                        if pk[2]['product_id'] == record.product_id.id :
                            pk[2]['quantity'] = qty_var
                            
        self.invoice_line_ids.sudo().unlink()
        self.invoice_line_ids = pack
        for stock_picking_tt_id in self.stock_picking_tt_ids :
            if stock_picking_tt_id :
                stock_picking_tt_id.invoice_id = self.id
        x = 1

    

    
    

    

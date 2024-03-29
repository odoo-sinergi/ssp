from odoo import api, fields, models, _ , SUPERUSER_ID
#from odoo.addons.product.models import decimal_precision as dp
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
from lxml import etree
class AccountMove(models.Model):
    _inherit='account.move'

    # picking_tt_ids = fields.Many2many(string='Stock Picking DO',comodel_name='stock.picking', relation='account_move_stock_picking_tt',column1='move_id',column2='Picking_tt_id',)
    # fields fix
    stock_picking_tt_ids = fields.Many2many(string='DO',comodel_name='stock.picking', relation='account_picking_tt_rel',column1='move_id',column2='picking_id',)
    stock_picking_po_ids = fields.Many2many(string='RO',comodel_name='stock.picking', relation='account_picking_po_rel',column1='move_id',column2='picking_id',)
    # picking_tt = fields.Boolean(string='Picking DO',)
    sale_id = fields.Many2one(comodel_name='sale.order',string='Sales Order',store=True)
    sale_procurement_group_id = fields.Many2one(comodel_name='procurement.group',string='Sale Procurement Group', related='sale_id.procurement_group_id',readonly=True, store=True)
    po_id = fields.Many2one(comodel_name='purchase.order',string='Purchase Order',store=True)
    purchase_procurement_group_id = fields.Many2one(comodel_name='procurement.group',string='Purchase Procurement Group', related='po_id.group_id',readonly=True, store=True)
    is_generate = fields.Selection(string='is_generate', selection=[('y', 'Y'), ('n', 'N')], default='n')
    total_pph = fields.Float(string='Total PPH',compute='_compute_total_pph')
    ppn = fields.Float(string='PPN',compute='_compute_total_pph')
    # invoice_no = fields.Char(string='Invoice No',)
    
   

    def unlink_move_line (self):
        self.invoice_line_ids.unlink()
        self.create_invoice_line()
    
    def unlink_invoice_number_picking (self):
        if self.sale_id :
            for stock_picking_tt_id in self.stock_picking_tt_ids :
                if stock_picking_tt_id :
                    stock_picking_tt_id.invoice_id = False
            self.invoice_line_ids.sudo().unlink()
            self.stock_picking_tt_ids = False

        if self.po_id :
            for stock_picking_po_id in self.stock_picking_po_ids :
                if stock_picking_po_id :
                    stock_picking_po_id.invoice_id = False
            self.invoice_line_ids.sudo().unlink()
            self.stock_picking_po_ids = False
        self.is_generate = 'n'
        
    
    def action_post(self):
        res = super().action_post()
        for data in self:
            if self.sale_id :
                for stock_picking_tt_id in data.stock_picking_tt_ids :
                    if stock_picking_tt_id :
                        stock_picking_tt_id.invoice_id = data.id
            if self.po_id :
                for stock_picking_po_id in data.stock_picking_po_ids :
                    if stock_picking_po_id :
                        stock_picking_po_id.invoice_id = data.id
        return res
    
    def button_cancel(self):
        res = super().button_cancel()
        for data in self:
            if data.stock_picking_tt_ids :
                for stock_picking_tt_id in data.stock_picking_tt_ids :
                    if stock_picking_tt_id.invoice_id :
                        stock_picking_tt_id.invoice_id = False
            if data.stock_picking_po_ids :
                for stock_picking_po_id in data.stock_picking_po_ids :
                    if stock_picking_po_id.invoice_id :
                        stock_picking_po_id.invoice_id = False
        return res

    # @api.onchange('stock_picking_tt_ids')
    # def onchange_stock_picking_tt_ids(self):
    #     for stock_picking_tt_id in self.stock_picking_tt_ids :
    #         if stock_picking_tt_id:
    #             order = stock_picking_tt_id.move_ids_without_package.sale_line_id.order_id
    #             partner = order.partner_invoice_id
    #             self.partner_id = partner.id
    #             self.invoice_date = stock_picking_tt_id.force_date
    #             self.date = stock_picking_tt_id.force_date
    #             self.invoice_payment_term_id = order.partner_id.property_payment_term_id
    #             self.ref = order.client_order_ref or ''
                
    # def create_invoice_line (self):
    #     aml_obj = self.env["account.move.line"]
    #     for stock_picking_tt_id in self.stock_picking_tt_ids :
    #         for stock_move in stock_picking_tt_id.move_ids_without_package :
    #             account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
    #             so_line = stock_move.sale_line_id
    #             invoices = aml_obj.create({
    #                 "name": so_line.name,
    #                 "move_id": self.id,
    #                 "account_id": account,
    #                 "price_unit": so_line.price_unit,
    #                 "quantity": stock_move.quantity_done,
    #                 "currency_id": so_line.currency_id.id,
    #                 "product_uom_id": so_line.product_uom.id,
    #                 "product_id": so_line.product_id.id,
    #                 "sale_line_ids": [(6, 0, so_line.ids)],
    #                 "tax_ids": [(6, 0, so_line.tax_id.ids)],
    #             })
    #     self.filter_invoice_line()

    # def create_invoice_line (self):
    #     aml_obj = self.env["account.move.line"]
    #     move_id = []
    #     for stock_picking_tt_id in self.stock_picking_tt_ids :
    #         for stock_move in stock_picking_tt_id.move_ids_without_package :
    #             move_id.append(stock_move.id )
    #             account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
    #             so_line = stock_move.sale_line_id
    #             invoices = aml_obj.create({
    #                 "name": so_line.name,
    #                 "move_id": self.id,
    #                 "account_id": account,
    #                 "price_unit": so_line.price_unit,
    #                 "quantity": stock_move.quantity_done,
    #                 "currency_id": so_line.currency_id.id,
    #                 "product_uom_id": so_line.product_uom.id,
    #                 "product_id": so_line.product_id.id,
    #                 "sale_line_ids": [(6, 0, so_line.ids)],
    #                 "tax_ids": [(6, 0, so_line.tax_id.ids)],
    #             })
        
    #     if move_id:
    #         stock_move_2 = self.env['stock.move'].search([('origin_returned_move_id', 'in', tuple(move_id))])
    #         if stock_move_2 :
    #             for sm2 in stock_move_2 :
    #                 account_2 = sm2.product_id.property_account_income_id.id or sm2.product_id.categ_id.property_account_income_categ_id.id
    #                 so_line_2 = sm2.sale_line_id
    #                 invoices = aml_obj.create({
    #                     "name": so_line_2.name,
    #                     "move_id": self.id,
    #                     "account_id": account_2,
    #                     "price_unit": so_line_2.price_unit,
    #                     "quantity": sm2.quantity_done * -1,
    #                     "currency_id": so_line_2.currency_id.id,
    #                     "product_uom_id": so_line_2.product_uom.id,
    #                     "product_id": so_line_2.product_id.id,
    #                     "sale_line_ids": [(6, 0, so_line_2.ids)],
    #                     "tax_ids": [(6, 0, so_line_2.tax_id.ids)],
    #                 })
    #     self.filter_invoice_line()

    # @api.model
    # def filter_invoice_line (self):
    #     pack = []
    #     total_qty = 0

    #     for record in self.invoice_line_ids:
    #         if not pack :
    #             total_qty = record.quantity
    #             total_qty = record.quantity
    #             pack.append((0,0,{
    #                 "name": record.name,
    #                 "move_id": record.id,
    #                 "account_id": record.account_id.id,
    #                 "price_unit": record.price_unit,
    #                 "quantity": record.quantity,
    #                 "currency_id": record.currency_id.id,
    #                 "product_uom_id": record.product_uom_id.id,
    #                 "product_id": record.product_id.id,
    #                 "sale_line_ids": [(4,record.sale_line_ids.id)],
    #                 "tax_ids": [(6, 0, record.tax_ids.ids)],
    #             }))
    #         else :
    #             check_data = [d for d in pack if d[2]['product_id'] == record.product_id.id]
    #             if not check_data :
    #                 total_qty = record.quantity
    #                 pack.append((0,0,{
    #                     "name": record.name,
    #                     "move_id": record.id,
    #                     "account_id": record.account_id.id,
    #                     "price_unit": record.price_unit,
    #                     "quantity": total_qty,
    #                     "currency_id": record.currency_id.id,
    #                     "product_uom_id": record.product_uom_id.id,
    #                     "product_id": record.product_id.id,
    #                     "sale_line_ids": [(4, record.sale_line_ids.id)],
    #                     "tax_ids": [(6, 0, record.tax_ids.ids)],
    #                 }))
    #             else :
    #                 qty_var = check_data[0][2]['quantity'] + record.quantity
    #                 for pk in pack :
    #                     if pk[2]['product_id'] == record.product_id.id :
    #                         pk[2]['quantity'] = qty_var
                            
    #     self.invoice_line_ids.sudo().unlink()
    #     self.invoice_line_ids = pack
    #     for stock_picking_tt_id in self.stock_picking_tt_ids :
    #         if stock_picking_tt_id :
    #             stock_picking_tt_id.invoice_id = self.id
    #     x = 1

    
    # def create_invoice_line (self):
    #     aml_obj = self.env["account.move.line"]
    #     move_id = []
    #     semua_data_invoice = []
    #     for stock_picking_tt_id in self.stock_picking_tt_ids :
    #         for stock_move in stock_picking_tt_id.move_ids_without_package :
    #             move_id.append(stock_move.id )
    #             account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
    #             so_line = stock_move.sale_line_id
    #             semua_data_invoice.append((0,0,{
    #                 "name": so_line.name,
    #                 "move_id": self.id,
    #                 "account_id": account,
    #                 "price_unit": so_line.price_unit,
    #                 "quantity": stock_move.quantity_done,
    #                 "currency_id": so_line.currency_id.id,
    #                 "product_uom_id": so_line.product_uom.id,
    #                 "product_id": so_line.product_id.id,
    #                 "sale_line_ids": [(6, 0, so_line.ids)],
    #                 "tax_ids": [(6, 0, so_line.tax_id.ids)],
    #             }))

    #     if move_id:
    #         stock_move_2 = self.env['stock.move'].search([('origin_returned_move_id', 'in', tuple(move_id))])
    #         if stock_move_2 :
    #             for sm2 in stock_move_2 :
    #                 account_2 = sm2.product_id.property_account_income_id.id or sm2.product_id.categ_id.property_account_income_categ_id.id
    #                 so_line_2 = sm2.sale_line_id
    #                 semua_data_invoice.append((0,0,{
    #                     "name": so_line_2.name,
    #                     "move_id": self.id,
    #                     "account_id": account_2,
    #                     "price_unit": so_line_2.price_unit,
    #                     "quantity": sm2.quantity_done * -1,
    #                     "currency_id": so_line_2.currency_id.id,
    #                     "product_uom_id": so_line_2.product_uom.id,
    #                     "product_id": so_line_2.product_id.id,
    #                     "sale_line_ids": [(6, 0, so_line_2.ids)],
    #                     "tax_ids": [(6, 0, so_line_2.tax_id.ids)],
    #                 }))
        
    #     # pack= []
    #     # for record in semua_data_invoice:
    #     #     total_qty = record[2]['quantity']
    #     #     pack.append((0,0,{
    #     #         "name": record[2]['name'],
    #     #         "move_id": record[2]['move_id'],
    #     #         "account_id": record[2]['account_id'],
    #     #         "price_unit": record[2]['price_unit'],
    #     #         "quantity": record[2]['quantity'],
    #     #         "currency_id": record[2]['currency_id'],
    #     #         "product_uom_id": record[2]['product_uom_id'],
    #     #         "product_id": record[2]['product_id'],
    #     #         "sale_line_ids": record[2]['sale_line_ids'],
    #     #         "tax_ids": record[2]['tax_ids'],
    #     #     }))

    #     pack= []
    #     for record in semua_data_invoice:
    #         if not pack :
    #             total_qty = record[2]['quantity']
    #             pack.append((0,0,{
    #                 "name": record[2]['name'],
    #                 "move_id": record[2]['move_id'],
    #                 "account_id": record[2]['account_id'],
    #                 "price_unit": record[2]['price_unit'],
    #                 "quantity": record[2]['quantity'],
    #                 "currency_id": record[2]['currency_id'],
    #                 "product_uom_id": record[2]['product_uom_id'],
    #                 "product_id": record[2]['product_id'],
    #                 "sale_line_ids": record[2]['sale_line_ids'],
    #                 "tax_ids": record[2]['tax_ids'],
    #             }))
    #         else :
    #             check_data = [d for d in pack if d[2]['product_id'] == record[2]['product_id'] and d[2]['price_unit'] == record[2]['price_unit'] and d[2]['name'] == record[2]['name']]
    #             if not check_data :
    #                 pack.append((0,0,{
    #                     "name": record[2]['name'],
    #                     "move_id": record[2]['move_id'],
    #                     "account_id": record[2]['account_id'],
    #                     "price_unit": record[2]['price_unit'],
    #                     "quantity": record[2]['quantity'],
    #                     "currency_id": record[2]['currency_id'],
    #                     "product_uom_id": record[2]['product_uom_id'],
    #                     "product_id": record[2]['product_id'],
    #                     "sale_line_ids": record[2]['sale_line_ids'],
    #                     "tax_ids": record[2]['tax_ids'],
    #                 }))
    #             else :
    #                 qty_var = check_data[0][2]['quantity'] + record[2]['quantity']
    #                 for pk in pack :
    #                     if pk[2]['product_id'] == record[2]['product_id'] and pk[2]['price_unit'] == record[2]['price_unit'] and pk[2]['name'] == record[2]['name'] :
    #                         pk[2]['quantity'] = qty_var
                            
    #     self.invoice_line_ids = pack
    #     for stock_picking_tt_id in self.stock_picking_tt_ids :
    #         if stock_picking_tt_id :
    #             stock_picking_tt_id.invoice_id = self.id
    #     x = 1
    
    
    def create_invoice_line (self):
        if self.sale_id :
            aml_obj = self.env["account.move.line"]
            move_id = []
            semua_data_invoice = []
            for stock_picking_tt_id in self.stock_picking_tt_ids :
                stock_picking_tt_id.ambil_move_line()
                for stock_move in stock_picking_tt_id.move_ids_without_package :
                    move_id.append(stock_move.id )
                    if stock_move.product_id.categ_id.property_valuation == 'real_time':
                        account = stock_move.product_id.categ_id.property_account_income_categ_id.id
                    else:
                        account = account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
                    # account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
                    so_line = stock_move.sale_line_id
                    semua_data_invoice.append((0,0,{
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
                    }))

            if move_id:
                stock_move_2 = self.env['stock.move'].search([('origin_returned_move_id', 'in', tuple(move_id))])
                if stock_move_2 :
                    for sm2 in stock_move_2 :
                        account_2 = sm2.product_id.property_account_income_id.id or sm2.product_id.categ_id.property_account_income_categ_id.id
                        so_line_2 = sm2.sale_line_id
                        semua_data_invoice.append((0,0,{
                            "name": so_line_2.name,
                            "move_id": self.id,
                            "account_id": account_2,
                            "price_unit": so_line_2.price_unit,
                            "quantity": sm2.quantity_done * -1,
                            "currency_id": so_line_2.currency_id.id,
                            "product_uom_id": so_line_2.product_uom.id,
                            "product_id": so_line_2.product_id.id,
                            "sale_line_ids": [(6, 0, so_line_2.ids)],
                            "tax_ids": [(6, 0, so_line_2.tax_id.ids)],
                        }))
            pack= []
            for record in semua_data_invoice:
                if not pack :
                    total_qty = record[2]['quantity']
                    pack.append((0,0,{
                        "name": record[2]['name'],
                        "move_id": record[2]['move_id'],
                        "account_id": record[2]['account_id'],
                        "price_unit": record[2]['price_unit'],
                        "quantity": record[2]['quantity'],
                        "currency_id": record[2]['currency_id'],
                        "product_uom_id": record[2]['product_uom_id'],
                        "product_id": record[2]['product_id'],
                        "sale_line_ids": record[2]['sale_line_ids'],
                        "tax_ids": record[2]['tax_ids'],
                    }))
                else :
                    check_data = [d for d in pack if d[2]['product_id'] == record[2]['product_id'] and d[2]['price_unit'] == record[2]['price_unit'] and d[2]['name'] == record[2]['name']]
                    if not check_data :
                        pack.append((0,0,{
                            "name": record[2]['name'],
                            "move_id": record[2]['move_id'],
                            "account_id": record[2]['account_id'],
                            "price_unit": record[2]['price_unit'],
                            "quantity": record[2]['quantity'],
                            "currency_id": record[2]['currency_id'],
                            "product_uom_id": record[2]['product_uom_id'],
                            "product_id": record[2]['product_id'],
                            "sale_line_ids": record[2]['sale_line_ids'],
                            "tax_ids": record[2]['tax_ids'],
                        }))
                    else :
                        qty_var = check_data[0][2]['quantity'] + record[2]['quantity']
                        for pk in pack :
                            if pk[2]['product_id'] == record[2]['product_id'] and pk[2]['price_unit'] == record[2]['price_unit'] and pk[2]['name'] == record[2]['name'] :
                                pk[2]['quantity'] = qty_var
                                
            self.invoice_line_ids = pack
            # SO
            for stock_picking_tt_id in self.stock_picking_tt_ids :
                if stock_picking_tt_id :
                    stock_picking_tt_id.invoice_id = self.id
            x = 1
        # PO
        if self.po_id :
            aml_obj = self.env["account.move.line"]
            move_id = []
            semua_data_invoice = []
            for stock_picking_tt_id in self.stock_picking_po_ids :
                for stock_move in stock_picking_tt_id.move_ids_without_package :
                    move_id.append(stock_move.id )

                    # account = stock_move.product_id.property_account_income_id.id or stock_move.product_id.categ_id.property_account_income_categ_id.id
                    if stock_move.product_id.categ_id.property_valuation == 'real_time':
                        account = stock_move.product_id.categ_id.property_stock_account_input_categ_id.id
                    else:
                        account = stock_move.product_id.categ_id.property_account_expense_categ_id.id
                    po_line = stock_move.purchase_line_id
                    semua_data_invoice.append((0,0,{
                        "name": po_line.name,
                        "move_id": self.id,
                        "account_id": account,
                        "price_unit": po_line.price_unit,
                        "quantity": stock_move.quantity_done,
                        "currency_id": po_line.currency_id.id,
                        "product_uom_id": po_line.product_uom.id,
                        "product_id": po_line.product_id.id,
                        # "purchase_line_id": [(6, 0, po_line.ids)],
                        "purchase_line_id": po_line.id,
                        "tax_ids": [(6, 0, po_line.taxes_id.ids)],
                    }))

            if move_id:
                stock_move_2 = self.env['stock.move'].search([('origin_returned_move_id', 'in', tuple(move_id))])
                if stock_move_2 :
                    for sm2 in stock_move_2 :
                        if sm2.product_id.categ_id.property_valuation == 'real_time':
                            account_2 = sm2.product_id.categ_id.property_stock_account_input_categ_id.id
                        else:
                            account_2 = sm2.product_id.categ_id.property_account_expense_categ_id.id
                        po_line_2 = sm2.purchase_line_id
                        semua_data_invoice.append((0,0,{
                            "name": po_line_2.name,
                            "move_id": self.id,
                            "account_id": account_2,
                            "price_unit": po_line_2.price_unit,
                            "quantity": sm2.quantity_done * -1,
                            "currency_id": po_line_2.currency_id.id,
                            "product_uom_id": po_line_2.product_uom.id,
                            "product_id": po_line_2.product_id.id,
                            "purchase_line_id": po_line_2.id,
                            "tax_ids": [(6, 0, po_line_2.taxes_id.ids)],
                        }))
            pack= []
            for record in semua_data_invoice:
                if not pack :
                    total_qty = record[2]['quantity']
                    pack.append((0,0,{
                        "name": record[2]['name'],
                        "move_id": record[2]['move_id'],
                        "account_id": record[2]['account_id'],
                        "price_unit": record[2]['price_unit'],
                        "quantity": record[2]['quantity'],
                        "currency_id": record[2]['currency_id'],
                        "product_uom_id": record[2]['product_uom_id'],
                        "product_id": record[2]['product_id'],
                        "purchase_line_id": record[2]['purchase_line_id'],
                        "tax_ids": record[2]['tax_ids'],
                    }))
                else :
                    check_data = [d for d in pack if d[2]['product_id'] == record[2]['product_id'] and d[2]['price_unit'] == record[2]['price_unit'] and d[2]['name'] == record[2]['name']]
                    if not check_data :
                        pack.append((0,0,{
                            "name": record[2]['name'],
                            "move_id": record[2]['move_id'],
                            "account_id": record[2]['account_id'],
                            "price_unit": record[2]['price_unit'],
                            "quantity": record[2]['quantity'],
                            "currency_id": record[2]['currency_id'],
                            "product_uom_id": record[2]['product_uom_id'],
                            "product_id": record[2]['product_id'],
                            "purchase_line_id": record[2]['purchase_line_id'],
                            "tax_ids": record[2]['tax_ids'],
                        }))
                    else :
                        qty_var = check_data[0][2]['quantity'] + record[2]['quantity']
                        for pk in pack :
                            if pk[2]['product_id'] == record[2]['product_id'] and pk[2]['price_unit'] == record[2]['price_unit'] and pk[2]['name'] == record[2]['name'] :
                                pk[2]['quantity'] = qty_var
                                
            self.invoice_line_ids = pack
            self.invoice_date = datetime.today().strftime('%Y-%m-%d')
            # PO
            for stock_picking_po_id in self.stock_picking_po_ids :
                if stock_picking_po_id :
                    stock_picking_po_id.invoice_id = self.id
            x = 1
        self.is_generate = 'y'
    
    
    @api.depends('line_ids','invoice_line_ids')  
    def _compute_total_pph(self):
        for i in self :
            total_pph = 0.0
            for line in i.line_ids:
                if line.account_id.code == '155.200' :
                    total_pph = line.debit

            if i.amount_tax - i.total_pph > 0 :
                i.update({
                    'total_pph' : total_pph,
                    'ppn' : i.amount_tax - i.total_pph
                })
            else :
                i.update({
                    'total_pph' : total_pph,
                    'ppn' : 0.0
                })
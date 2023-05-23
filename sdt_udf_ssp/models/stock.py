from odoo import fields, models, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit='stock.picking'

    # work_base_structure = fields.Many2one('account.analytic.account', string='Work Base Structure')
    jitcall = fields.Char(string='JIT Call')
    picking_do_id = fields.Many2one('stock.picking',string='Picking DO',)
    invoice_id = fields.Many2one('account.move',string='No. Invoice',)
    is_picking_do_id = fields.Boolean(string='Picking DO',)
    no_polisi = fields.Char(string='No. Pol')
    driver = fields.Char(string='Driver')
    procurement_group_id = fields.Integer(string='Procurement Group', related='group_id.id', readonly=True, store=True )
    surat_jalan = fields.Char(string='Surat Jalan',)
    client_order_ref = fields.Char(string='Customer Reference',)


    # @api.onchange('move_ids_without_package')
    # def _onchange_move_ids_without_package(self):
    #     for i in self :
    #         if i.picking_type_code == 'incoming':
    #             if i.group_id :
    #                 for move_ids in i.move_ids_without_package :
    #                     if move_ids.quantity_done > move_ids.product_uom_qty :
    #                         raise UserError(_("Qty Done tidak boleh lebih besar dari pada Qty Demand !!"))
    #             else :
    #                 pass
    #         else :
    #             pass       

    
    # @api.onchange('picking_do_id','is_picking_do_id')
    # def onchange_picking_do_id(self):
    #     if self.is_picking_do_id:
    #         picking_obj = self.env['stock.picking'].search([('group_id', '=', self.group_id.id),('picking_type_code', '=', 'internal')])
    #         picking_list=[]
    #         for line in picking_obj:
    #             picking_list.append(line.id)
    #         domain = {'picking_do_id': [('id', '=', picking_list)]}
    #         return {'domain': domain}
    #     else :
    #         pass
    
    # def get_line (self) :
    #     self.move_ids_without_package._action_cancel()
    #     self.move_ids_without_package.unlink()
    #     move_id=[]
    #     picking_obj = self.picking_do_id
    #     for move_id_without_package in picking_obj.move_ids_without_package:
    #         if move_id_without_package :
    #             product_id = move_id_without_package.product_id.id
    #             location_id = self.picking_do_id.location_id.id
    #             location_dest_id = self.picking_do_id.location_dest_id.id
    #             partner_id = self.picking_do_id.partner_id.id
    #             picking_id = self.picking_do_id.id
    #             group_id = self.picking_do_id.group_id.id
    #             rule_id = 10
    #             picking_type_id = self.picking_do_id.picking_type_id.id
    #             warehouse_id = move_id_without_package.warehouse_id.id
    #             name = move_id_without_package.product_id.name
    #             state = 'partially_available'
    #             origin = self.picking_do_id.origin
    #             procure_method = 'make_to_order'
    #             reference = self.name
    #             description_picking = move_id_without_package.description_picking
    #             product_uom_qty = move_id_without_package.quantity_done
    #             company_id = move_id_without_package.company_id.id
    #             date = move_id_without_package.date
    #             product_uom = move_id_without_package.product_uom.id
    #         hasil={
    #             'product_id' : product_id,
    #             'location_id' : location_id,
    #             'location_dest_id' : location_dest_id,
    #             'partner_id' : partner_id,
    #             'picking_id' : picking_id,
    #             'group_id' : group_id,
    #             'rule_id' : rule_id,
    #             'picking_type_id' : picking_type_id,
    #             'warehouse_id' : warehouse_id,
    #             'name' : name,
    #             'state' : state,
    #             'origin' : origin,
    #             'procure_method' : procure_method,
    #             'reference' : reference,
    #             'description_picking' : description_picking,
    #             'product_uom_qty' : product_uom_qty,
    #             'company_id' : company_id,
    #             'date' : date,
    #             'product_uom' : product_uom,
    #         }
    #     move_id.append((0,0,hasil))
    #     self.move_ids_without_package = move_id
    
    # def button_validate(self):
    #     res = super().button_validate()
    #     for data in self:
    #         if data.work_base_structure.id:
    #             all_analytic = {}
    #             all_analytic.update({str(data.work_base_structure.id) : 100})
    #             for move in data.move_id_without_packages:
    #                 for value in move.stock_valuation_layer_ids:
    #                     for amv in value.account_move_id_without_package:
    #                         for amlv in amv.line_ids:
    #                             amlv.analytic_distribution = all_analytic
    #     return res


class StockMove(models.Model):
    _inherit='stock.move'

    

    


    


    
    

    

from odoo import fields, models, api, _
from odoo.exceptions import UserError
    

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for i in self :
            if i.picking_ids :
                for picking_id in i.picking_ids.filtered(lambda l: l.state not in ['done','cancel']) :
                    for move in picking_id.move_ids_without_package:
                        move.outstanding = move.purchase_line_id.outstanding
        return res
    
    @api.model
    def _get_picking_type(self, company_id):
        picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('id', '=', 1)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id.company_id', '=', company_id)])
        if not picking_type:
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming'), ('warehouse_id', '=', False)])
        return picking_type[:1]
    
class PurchaseOrderLine(models.Model):
    _inherit='purchase.order.line'

    outstanding = fields.Float(string='Outstanding', compute='_get_outstanding')

    @api.depends('qty_received','product_uom_qty')
    def _get_outstanding(self):
        for rec in self:
            if rec.qty_received:
                rec.outstanding = rec.product_uom_qty - rec.qty_received
                for move_id in rec.move_ids.filtered(lambda l: l.state not in ['done','cancel']):
                    move_id.outstanding = rec.outstanding
            else:
                rec.outstanding = rec.product_uom_qty

    
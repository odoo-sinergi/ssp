from odoo import fields, models, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for i in self :
            if i.picking_ids :
                for picking_id in i.picking_ids.filtered(lambda l: l.state not in ['done','cancel']) :
                    picking_id.client_order_ref = i.client_order_ref
                    for move in picking_id.move_ids_without_package:
                        move.outstanding = move.sale_line_id.outstanding
        return res

class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    outstanding = fields.Float(string='Outstanding', compute='_get_outstanding')
    
    @api.depends('qty_delivered','product_uom_qty')
    def _get_outstanding(self):
        for rec in self:
            if rec.qty_delivered:
                rec.outstanding = rec.product_uom_qty - rec.qty_delivered
                for move_id in rec.move_ids.filtered(lambda l: l.state not in ['done','cancel']):
                    move_id.outstanding = rec.outstanding
            else:
                rec.outstanding = rec.product_uom_qty

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

    
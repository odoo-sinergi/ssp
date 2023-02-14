from odoo import fields, models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit='purchase.order'

    for_department = fields.Boolean(string='For Department', compute='_compute_for_analytic')
    for_project = fields.Boolean(string='For Project', compute='_compute_for_analytic')
    for_location = fields.Boolean(string='For Location', compute='_compute_for_analytic')

    @api.depends('order_line.analytic_department_id','order_line.analytic_project_id','order_line.product_id')
    def _compute_for_analytic(self):
        for data in self:
            for_department = False
            for_project = False
            for_location = False
            if data.order_line and all(p.analytic_department_id for p in data.order_line.filtered(lambda x: x.product_id)):
                for_department = True
            if data.order_line and all(p.analytic_project_id for p in data.order_line.filtered(lambda x: x.product_id)):
                for_project = True
            if data.order_line and all(p.for_location for p in data.order_line.filtered(lambda x: x.product_id)):
                for_location = True
            data.for_project = for_project
            data.for_department = for_department
            data.for_location = for_location

    
class PurchaseOrderLine(models.Model):
    _inherit='purchase.order.line'

    for_project = fields.Boolean(string='For Project')
    for_department = fields.Boolean(string='For Department')
    for_location = fields.Boolean(string='For Location')
    spesifikasi = fields.Char(related='product_id.product_tmpl_id.spesifikasi', string='Spesifikasi', readonly=True, store=True)
    merk = fields.Char(related='product_id.product_tmpl_id.merk', string='Merk', readonly=True)
    analytic_department_id = fields.Many2one('account.analytic.account', string='Analytic Department', domain="[('plan_name','=','0002 Departments')]")
    analytic_project_id = fields.Many2one('account.analytic.account', string='Analytic Project', domain="[('plan_name','=','0001 Projects')]")
    analytic_location_id = fields.Many2one('account.analytic.account', string='Analytic Location', domain="[('plan_name','=','0003 Locations')]")

    @api.onchange('product_id','analytic_distribution')
    def _onchange_for_analytic(self):
        for data in self:
            data.analytic_distribution

    @api.onchange('product_id','analytic_department_id','analytic_project_id')
    def _onchange_sdt_analytic(self):
        for data in self:
            all_analytic = {}
            for dep in data.analytic_department_id:
                all_analytic.update({str(data.analytic_department_id.id) : 100})
            for dep in data.analytic_project_id:
                all_analytic.update({str(data.analytic_project_id.id) : 100})
            for dep in data.analytic_location_id:
                all_analytic.update({str(data.analytic_location_id.id) : 100})
            data.analytic_distribution = all_analytic



# class PurchaseAdvancePaymentInv(models.TransientModel):
#     _inherit = "purchase.advance.payment.inv"

#     def create_vendor_bills(self):
#         purchase_orders = self.env["purchase.order"].browse(
#             self._context.get("active_ids", [])
#         )
#         company_id = purchase_orders.mapped('company_id')
#         if company_id:
#             self = self.with_context(force_company=company_id.id, default_company_id=company_id.id)
#         if self.advance_payment_method == "delivered":
#             self.check_invoice_status(purchase_orders)
#             self.env.context = dict(self.env.context)
#             self.env.context.update({"without_downpayment": True})
#             journal_id = self.env["account.journal"].search(
#                 [("type", "in", ["purchase"]), ("company_id", "=", company_id.id)], limit=1
#             )
#             inv = self.env["account.move"].create({"move_type": "in_invoice", "journal_id":journal_id.id})
#             inv.update({"purchase_id": purchase_orders.id})
#             inv._onchange_purchase_auto_complete()
#             if all(
#                 line.purchase_line_id.is_downpayment for line in inv.invoice_line_ids
#             ):
#                 for line in inv.invoice_line_ids:
#                     line.quantity = 1
#                 inv.move_type = "in_refund"
#         elif self.advance_payment_method == "all":
#             if not any(line.is_downpayment for line in purchase_orders.order_line):
#                 self.check_invoice_status(purchase_orders)
#             self.env.context = dict(self.env.context)
#             self.env.context.update({"final": True, "final_payment": True})
#             journal_id = self.env["account.journal"].search(
#                 [("type", "in", ["purchase"]), ("company_id", "=", company_id.id)], limit=1
#             )
#             inv = self.env["account.move"].create({"move_type": "in_invoice", "journal_id":journal_id.id})
#             inv.update({"purchase_id": purchase_orders.id})
#             inv._onchange_purchase_auto_complete()
#             if all(
#                 line.purchase_line_id.is_downpayment for line in inv.invoice_line_ids
#             ):
#                 for line in inv.invoice_line_ids:
#                     line.quantity = 1
#                 inv.move_type = "in_refund"
#         else:
#             purchase_line_obj = self.env["purchase.order.line"]
#             for order in purchase_orders:
#                 if self.advance_payment_method == "percentage":
#                     amount = order.amount_untaxed * self.amount / 100
#                 else:
#                     amount = self.amount
#                 if self.product_id.purchase_method != "purchase":
#                     raise UserError(
#                         _(
#                             'The down payment product should have a control policy set to "Ordered quantities". Please update your down payment product.'
#                         )
#                     )
#                 if self.product_id.type != "service":
#                     raise UserError(
#                         _(
#                             "The down payment product should be of type 'Service'. Please use another product or update this product."
#                         )
#                     )
#                 taxes = self.product_id.taxes_id.filtered(
#                     lambda r: not order.company_id or r.company_id == order.company_id
#                 )
#                 if order.fiscal_position_id and taxes:
#                     tax_ids = order.fiscal_position_id.map_tax(
#                         taxes, self.product_id, order.partner_id
#                     ).ids
#                 else:
#                     tax_ids = taxes.ids
#                 context = {"lang": order.partner_id.lang}
#                 analytic_tag_ids = []
#                 for line in order.order_line:
#                     analytic_tag_ids = [
#                         (4, analytic_tag.id, None)
#                         for analytic_tag in line.analytic_tag_ids
#                     ]
#                 po_line = purchase_line_obj.create(
#                     {
#                         "name": _("Advance: %s") % (time.strftime("%m %Y"),),
#                         "price_unit": amount,
#                         "product_qty": 0.0,
#                         "order_id": order.id,
#                         "product_uom": self.product_id.uom_id.id,
#                         "product_id": self.product_id.id,
#                         "analytic_tag_ids": analytic_tag_ids,
#                         "taxes_id": [(6, 0, tax_ids)],
#                         "is_downpayment": True,
#                         "date_planned": order.date_order,
#                     }
#                 )
#                 del context
#                 self._create_invoice(order, po_line, amount)
#         ctx =  dict(self.env.context)
#         ctx['purchase_bill'] = True
#         purchase_orders = purchase_orders.with_context(ctx)
#         if self._context.get("create_bill", False):
#             return purchase_orders.action_view_invoice()
#         return {"type": "ir.actions.act_window_close"}
                    


    


    
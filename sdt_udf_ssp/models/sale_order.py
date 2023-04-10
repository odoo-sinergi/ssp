from odoo import fields, models, api, _

class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        invoice = self.env['account.move'].search([('invoice_origin', '=', sale_orders.name)])
        for order in self:
            if invoice :
                for inv in invoice :
                    inv.ref = sale_orders.client_order_ref
        return res
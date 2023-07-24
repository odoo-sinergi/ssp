from odoo import models, fields, api, exceptions, _
from . import terbilang
from . import convert_day

class AccountMove(models.Model):
    _inherit = "account.move"
    _template = 'form_standard_odoo.standard_sales_invoice_document'

    def terbilang_idr(self):
        return terbilang.terbilang(self.amount_total, 'idr', 'en')

    def render_html(self, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name(self._template)
        docargs = {
            'terbilang_idr': self.terbilang_idr,
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render(self._template, docargs)
    

    def get_day(self, date):
        return convert_day.get_day(date, 'id')

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    _template = 'form_standard_odoo.standard_lampiran_do_document'

    def _get_initial(self, product_line):
        len_product_line = len(product_line.ids)
        return len_product_line
    
    def cek_qty(self, move_id):
        line_retur = self.env['stock.move'].search([('origin_returned_move_id', '=', move_id.id)])
        if not line_retur:
            if move_id.quantity_done > 0:
                return move_id.quantity_done
        else:
            qty_retur = sum(line_retur.mapped("quantity_done"))
            qty = move_id.quantity_done - qty_retur
            return qty
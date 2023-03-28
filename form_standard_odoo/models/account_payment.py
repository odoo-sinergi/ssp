from odoo import models, fields, api, exceptions, _
from . import terbilang
from . import convert_day

class AccountPayment(models.Model):
    _inherit = "account.payment"
    _template = 'form_standard_odoo.payment_report_document'

    description = fields.Text(string='Description',)
    bill_id = fields.Many2one('account.move',string='Bill',)
    
    def terbilang_idr(self):
        return terbilang.terbilang(self.amount, 'idr', 'id')

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
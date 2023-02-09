from odoo import fields, models, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    n_ppn = fields.Selection([('YES','YES'),
                              ('NO','NO')],string='PPN')


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'


    def _create_payments(self):
        res = super()._create_payments()
        for r in res:
            if r.reconciled_invoice_ids:
                r.n_ppn = r.reconciled_invoice_ids.n_ppn
            if r.reconciled_bill_ids: 
                r.n_ppn = r.reconciled_bill_ids.n_ppn
        return res


    


    


    
    

    

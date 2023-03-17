from odoo import api, fields,models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class AccountPaymentRegister(models.TransientModel):
    _inherit='account.payment.register'

    description = fields.Text(string='Description',)


    def action_create_payments(self):
        planner = super(AccountPaymentRegister, self).action_create_payments()
        for i in self :
            account_payment_obj = i.env['account.payment'].search([('ref', '=', i.communication)])
            if account_payment_obj :
                account_payment_obj.description = i.description
        return planner
    
    # def _create_payment_vals_from_wizard(self):
    #     payment_vals = {
    #         'disc': self.disc,
    #         'date': self.payment_date,
    #         'amount': self.amount,
    #         'payment_type': self.payment_type,
    #         'partner_type': self.partner_type,
    #         'ref': self.communication,
    #         'journal_id': self.journal_id.id,
    #         'currency_id': self.currency_id.id,
    #         'partner_id': self.partner_id.id,
    #         'partner_bank_id': self.partner_bank_id.id,
    #         'payment_method_id': self.payment_method_id.id,
    #         'destination_account_id': self.line_ids[0].account_id.id,
    #     }

    #     if not self.currency_id.is_zero(self.payment_difference) and self.payment_difference_handling == 'reconcile':
    #         payment_vals['write_off_line_vals'] = {
    #             'name': self.writeoff_label,
    #             'amount': self.payment_difference,
    #             'account_id': self.writeoff_account_id.id,
    #         }
        
    #     if not self.communication :
    #         raise UserError(('Memo harus di isi'))

    #     return payment_vals
        
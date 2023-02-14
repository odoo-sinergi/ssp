from odoo import fields, models, api, _

class AccountMove(models.Model):
    _inherit='account.move'

    for_analytic = fields.Boolean(string='For Analytic', compute='_compute_for_analytic')

    @api.depends('invoice_line_ids.analytic_distribution','line_ids.analytic_distribution')
    def _compute_for_analytic(self):
        for data in self:
            for_analytic = False
            if data.line_ids and all(p.analytic_distribution for p in data.line_ids):
                for_analytic = True
            data.for_analytic = for_analytic

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for inv in res:
            if inv.move_type == 'entry':
                if not inv.partner_id:
                    partner_id = False
                    for line in inv.line_ids:
                        if partner_id == False:
                            # partner_id = inv.line_ids.filtered(lambda x: x.partner_id)[0].partner_id
                            partner_id = line.partner_id
                    inv.update({'partner_id':partner_id.id if partner_id else False})
        return res


class AccountMoveLine(models.Model):
    _inherit='account.move.line'


    spesifikasi = fields.Char(related='product_id.product_tmpl_id.spesifikasi', string='Spesifikasi', readonly=True, store=True)

    
    


    


    
    

    

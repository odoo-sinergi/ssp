from odoo import fields, models, api, _

class ResPartner(models.Model):
    _inherit='res.partner'

    n_ppn = fields.Selection([('YES','YES'),
                              ('NO','NO')],string='PPN')

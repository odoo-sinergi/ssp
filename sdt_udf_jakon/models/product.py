from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit='product.template'

    
    link_reference = fields.Char(string='Link Reference')
    spesifikasi = fields.Char(string='Spesifikasi')
    merk = fields.Char(string='Merk')


class ProductProduct(models.Model):
    _inherit='product.product'



    
    

    

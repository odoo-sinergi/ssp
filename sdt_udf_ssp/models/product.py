from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit='product.template'

    part_no = fields.Char(string='Part No.')




    
    

    

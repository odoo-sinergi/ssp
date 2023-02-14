from odoo import fields, models, api, _



class MrpBom(models.Model):
    _inherit='mrp.bom'

    
    
class MrpBomLine(models.Model):
    _inherit='mrp.bom.line'

    link_reference = fields.Char(related='product_id.product_tmpl_id.link_reference', string='Link Reference', readonly=True)



    
    

    

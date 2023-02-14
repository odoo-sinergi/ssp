from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit='sale.order'

    for_department = fields.Boolean(string='For Department', compute='_compute_for_analytic')
    for_project = fields.Boolean(string='For Project', compute='_compute_for_analytic')
    for_location = fields.Boolean(string='For Location', compute='_compute_for_analytic')

    @api.depends('order_line.analytic_department_id','order_line.analytic_project_id','order_line.product_id')
    def _compute_for_analytic(self):
        for data in self:
            for_department = False
            for_project = False
            for_location = False
            if data.order_line and all(p.analytic_department_id for p in data.order_line.filtered(lambda x: x.product_id)):
                for_department = True
            if data.order_line and all(p.analytic_project_id for p in data.order_line.filtered(lambda x: x.product_id)):
                for_project = True
            if data.order_line and all(p.analytic_location_id for p in data.order_line.filtered(lambda x: x.product_id)):
                for_location = True
            data.for_project = for_project
            data.for_department = for_department
            data.for_location = for_location



class SaleOrderLine(models.Model):
    _inherit='sale.order.line'

    spesifikasi = fields.Char(related='product_id.product_tmpl_id.spesifikasi', string='Spesifikasi', readonly=True, store=True)
    for_project = fields.Boolean(string='For Project')
    for_department = fields.Boolean(string='For Department')
    for_location = fields.Boolean(string='For Location')
    analytic_project_id = fields.Many2one('account.analytic.account', string='Analytic Project', domain="[('plan_name','=','0001 Projects')]")
    analytic_department_id = fields.Many2one('account.analytic.account', string='Analytic Department', domain="[('plan_name','=','0002 Departments')]")
    analytic_location_id = fields.Many2one('account.analytic.account', string='Analytic Location', domain="[('plan_name','=','0003 Locations')]")


    @api.onchange('product_id','analytic_department_id','analytic_project_id','analytic_location_id')
    def _onchange_sdt_analytic(self):
        for data in self:
            all_analytic = {}
            for dep in data.analytic_department_id:
                all_analytic.update({str(data.analytic_department_id.id) : 100})
            for dep in data.analytic_project_id:
                all_analytic.update({str(data.analytic_project_id.id) : 100})
            for dep in data.analytic_location_id:
                all_analytic.update({str(data.analytic_location_id.id) : 100})
            data.analytic_distribution = all_analytic

    


    


    
    

    

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import re

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.osv.expression import expression


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    
    analytic_department_id = fields.Many2one('account.analytic.account', 'Analytic Department', readonly=True, domain="[('plan_name','=','002 Departments')]")
    analytic_project_id = fields.Many2one('account.analytic.account', 'Analytic Project', readonly=True, domain="[('plan_name','=','001 Projects')]")
    analytic_location_id = fields.Many2one('account.analytic.account', 'Analytic Location', readonly=True, domain="[('plan_name','=','003 Locations')]")
   

    def _select(self):
        return super(PurchaseReport, self)._select() + ", l.analytic_department_id as analytic_department_id, l.analytic_project_id as analytic_project_id, l.analytic_location_id as analytic_location_id"

    # def _from(self):
    #     return super(PurchaseReport, self)._from() + " left join stock_picking_type spt on (spt.id=po.picking_type_id)"

    def _group_by(self):
        return super(PurchaseReport, self)._group_by() + ", l.analytic_department_id, l.analytic_project_id, l.analytic_location_id"

   
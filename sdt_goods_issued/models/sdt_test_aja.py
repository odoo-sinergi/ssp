# -*- coding: utf-8 -*-

from odoo import api, fields, models, _ , SUPERUSER_ID
#from odoo.addons.product.models import decimal_precision as dp
from odoo.addons import decimal_precision as dp
from  odoo.exceptions import UserError
from datetime import datetime
from datetime import timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_STATES = [
    ('open', 'Draft'),
    ('to_approved', 'To Be Approved'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('valid', 'Done'),
    ('canceled', 'Canceled')
]


class SDTTestAja(models.Model):
    _name = 'sdt.test.aja'
    _description = 'Test Aja'
    _order = 'date desc, name desc, id desc'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'sequence.mixin']


    name = fields.Char('Name', size=32, required=True, track_visibility='onchange',copy=True, index=True)
    date = fields.Date('Date', default=fields.Date.context_today, track_visibility='onchange')
    line_ids = fields.One2many('sdt.test.aja.line', 'test_id', string='Products to Issued', states={'open': [('readonly', False)]}, copy=True, readonly=True, check_company=True,)
    state = fields.Selection(selection=_STATES,string='Status',index=True,track_visibility='onchange',required=True,copy=False,default='open')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)
    
    


class SDTTestAjaLine(models.Model):
    _name = "sdt.test.aja.line"
    _description = "Test Aja Line"
    _order = "id desc, name desc"
    _rec_names_search = ['name', 'test_id', 'product_id']

    test_id = fields.Many2one(comodel_name='sdt.test.aja', string='Test Aja', ondelete='cascade', required=True, index=True, copy=False, auto_join=True, check_company=True)
    name = fields.Char('Description')
    sequence = fields.Integer(string='Sequence', default=10)
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    product_id = fields.Many2one('product.product', 'Material Name',domain=[('type', '=', 'product')])
    product_uom_id = fields.Many2one(comodel_name='uom.uom', inverse_name='id', string='UoM', store=True)
    company_id = fields.Many2one('res.company', required=True, related='test_id.company_id', store=True, default=lambda self: self.env.company)


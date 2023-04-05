from odoo import fields, models, api, _



class ResPartner(models.Model):
    _inherit='res.partner'

    siup = fields.Char(string="SIUP")
    tdp = fields.Char(string="TDP")
    nib = fields.Char(string="NIB")
    skt = fields.Char(string="SKT")
    sppkp = fields.Char(string="SPPKP")
    fax = fields.Char(string="Fax")
    # department = fields.Char(string="Department")

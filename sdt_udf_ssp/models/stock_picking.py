from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    status_do = fields.Char(string='Status DO',)
    
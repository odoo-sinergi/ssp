from odoo import api, fields, models, _ , SUPERUSER_ID
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    status_do = fields.Char(string='Status DO',)
    
    def button_validate(self):
        res = super().button_validate()
        self.ambil_move_line()
        return res

    def ambil_move_line(self):
        for i in self :
            for move_id_without_package in i.move_ids_without_package :
                if move_id_without_package.sdt_qty_return > 0 :
                    move_id_without_package.sdt_qty_done =  move_id_without_package.quantity_done -  move_id_without_package.sdt_qty_return
                else :
                    myquery ="select quantity " \
                    "from stock_return_picking_line "\
                    "where move_id=%s;"
                    self.env.cr.execute(myquery, (move_id_without_package.id,))
                    result = self.env.cr.dictfetchall()
                    total_return = 0.0
                    for res in result :
                        if res :
                            if total_return > 0.0 :
                                total_return = total_return + res['quantity']
                            else :
                                total_return = res['quantity']
                        else :
                            move_id_without_package.sdt_qty_done = move_id_without_package.quantity_done
                    move_id_without_package.sdt_qty_done = move_id_without_package.quantity_done - total_return
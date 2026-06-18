from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            for move in picking.move_ids:
                if move.product_uom_qty > move.product_id.qty_available:
                    raise ValidationError(
                        "The available quantity is less than the demand quantity"
                    )
        return super().button_validate()

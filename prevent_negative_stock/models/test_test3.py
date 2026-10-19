from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:

            if picking.picking_type_id.code != "outgoing":
                continue

            for move in picking.move_ids:
                available_quantity = move.product_id.with_context(
                    location = move.location_id.id
                ).qty_available

                if move.product_uom_qty > available_quantity:
                    raise ValidationError(
                        _(
                            "Not enough stock for product '%s'. "
                            "Available quantity: %s"
                        )
                        %
                        (
                            move.product_id.name,
                            available_quantity
                        )
                    )
        return super().button_validate()


from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_done(self, cancel_backorder=False):
        for move in self:
            product = move.product_id


            if not product.is_storable:
                continue

            if (product.allow_negative_stock or
                    product.categ_id.allow_negative_stock or
                    move.location_id.allow_negative_stock or
                    move.location_dest_id.allow_negative_stock):
                continue

            qty_on_hand = product.with_context(location=move.location_id.id).qty_available
            if float_compare(
                    qty_on_hand,
                    move.product_uom_qty,
                    precision_rounding=product.uom_id.rounding,
            ) < 0:
                raise UserError(_(
                    "Operation Not Allowed\n\n"
                    "Product: %s\n"
                    "Available: %.2f %s\n"
                    "Requires: %.2f %s\n\n"
                ) % (
                                    product.display_name,
                                    qty_on_hand, product.uom_id.name,
                                    move.product_uom_qty, product.uom_id.name
                                ))

        return super()._action_done(cancel_backorder=cancel_backorder)

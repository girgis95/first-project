from odoo import models, fields, api, _


class StockLocation(models.Model):
    _inherit = 'stock.location'

    allow_negative_stock = fields.Boolean(string='Allow Negative Stock',
                                          help='if checked, negative stock will be allowed for this category of products' )


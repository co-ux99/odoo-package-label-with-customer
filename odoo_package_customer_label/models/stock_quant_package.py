from odoo import models, fields, api


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    partner_id = fields.Many2one(
        'res.partner',
        string='Πελάτης',
        compute='_compute_partner_id',
    )

    picking_id = fields.Many2one(
        'stock.picking',
        string='Picking',
        compute='_compute_partner_id',
    )

    def _compute_partner_id(self):
        for package in self:
            move_line = self.env['stock.move.line'].search([
                '|',
                ('result_package_id', '=', package.id),
                ('package_id', '=', package.id)
            ], order='create_date desc', limit=1)
            
            if move_line and move_line.picking_id:
                package.picking_id = move_line.picking_id
                package.partner_id = move_line.picking_id.partner_id
            else:
                package.picking_id = False
                package.partner_id = False
# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class MrpProduction(models.Model):
    _inherit = "mrp.production"


    sale_line_id = fields.Many2one(
        comodel_name='sale.order.line', string='Sale Line',
        compute='_compute_sale_line_id', readonly=True, store=True)
    sale_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order',
        readonly=True, store=True,
        related='sale_line_id.order_id')
    partner_id = fields.Many2one(related='sale_id.partner_id',
                                 string='Customer', store=True)
    commitment_date = fields.Datetime(related='sale_id.commitment_date',
                                      string='Commitment Date', store=True)
    sale_note = fields.Text(
        string='Sale order Note',
        readonly=True, store=True,
        related='sale_id.note')

    @api.one
    @api.depends('move_prod_id')
    def _compute_sale_line_id(self):
        self.sale_line_id = self.move_prod_id.procurement_id.sale_line_id or self.move_prod_id.raw_material_production_id.move_prod_id.procurement_id.sale_line_id

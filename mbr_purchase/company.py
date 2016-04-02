# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models

class company(models.Model):
    _inherit = 'res.company'

    po_level_one_max_amount = fields.Monetary(string='Level one max amount', default=5000)
    po_level_two_max_amount = fields.Monetary(string='Level two max amount', default=10000)
    po_level_three_max_amount = fields.Monetary(string='Level three max amount', default=30000)
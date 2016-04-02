# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models

class company(models.Model):
    _inherit = 'res.company'

    so_level_one_max_discount = fields.Integer(string='Level one max discount', default=5)
    so_level_two_max_discount = fields.Integer(string='Level two max discount', default=7)

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import fields, models

class UsersAccess(models.Model):
    _inherit = 'res.users'
    user_access = fields.Many2many('stock.warehouse',string="user warehouse")
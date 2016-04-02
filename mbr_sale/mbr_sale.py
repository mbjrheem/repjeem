__author__ = 'Rheem'
from openerp import models,fields,api
from openerp import _
from openerp.exceptions import Warning
class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    @api.depends('order_line.discount')
    def _discount_total(self):
        for ln in self:
            total_discount = sum(s.discount for s in ln.order_line)
        ln.update({
                'discount_total': total_discount,
            })

    discount_total = fields.Integer(
        'total_discount',
        compute='_discount_total')


    @api.multi
    def action_confirm(self):
        if (self.discount_total <= self.env.user.company_id.so_level_one_max_discount and self.user_has_groups\
                    ('mbr_sale.group_sale_level_one_max_discount')):
            return super(SaleOrder, self).action_confirm()

        elif (self.discount_total <= self.env.user.company_id.so_level_two_max_discount and self.user_has_groups\
                    ('mbr_sale.group_sale_level_two_max_discount,mbr_sale.group_sale_level_one_max_discount')):
            return super(SaleOrder, self).action_confirm()

        elif (self.user_has_groups('mbr_sale.group_sale_director')):
            return super(SaleOrder, self).action_confirm()

        else:
            raise Warning(_('you are not allowed to confirm this order'))
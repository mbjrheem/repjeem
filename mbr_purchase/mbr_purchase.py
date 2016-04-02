__author__ = 'Rheem'
from openerp import *
from openerp import _
from openerp.exceptions import Warning


class CommitteeLog(models.Model):
    _name = 'committee.log'
    user_id = fields.Integer(string='comm user')
    po_id =   fields.Integer(string = 'PO id')
    po_confirm = fields.Boolean('committee confirm', default=True)
    po_cancel = fields.Boolean('committee cancel', default=False)
    #po_id = fields.Many2many('purchase.order',string='purchase order')



class PurchaseOrder(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order']
    committee = fields.Many2many('committee.log',string='committe log')

    @api.multi
    def button_confirm(self):
        if (self.amount_total <= self.env.user.company_id.currency_id.compute(self.company_id.po_level_one_max_amount, self.currency_id) \
                and (self.user_has_groups('mbr_purchase.group_purchase_level_one_max_amount,mbr_purchase.group_purchase_level_two_max_amount,mbr_purchase.group_purchase_level_three_max_amount'))):
            return super(PurchaseOrder, self).button_confirm()
        elif(self.amount_total <= self.env.user.company_id.currency_id.compute(self.company_id.po_level_two_max_amount, self.currency_id) \
                 and (self.user_has_groups('mbr_purchase.group_purchase_level_two_max_amount,mbr_purchase.group_purchase_level_three_max_amount'))):
            return super(PurchaseOrder, self).button_confirm()
        elif(self.amount_total <= self.env.user.company_id.currency_id.compute(self.company_id.po_level_three_max_amount, self.currency_id) \
                 and (self.user_has_groups('mbr_purchase.group_purchase_level_three_max_amount'))):
            return super(PurchaseOrder, self).button_confirm()
        elif(self.amount_total > self.env.user.company_id.currency_id.compute(self.company_id.po_level_three_max_amount, self.currency_id)):

            #get all users in committee log who's current users and and current po is po in committee log
            is_committee_did_approve = self.env['committee.log'].search([('user_id','=',self.env.uid),('po_id','=',self.id),('po_confirm','=',True)])

            #user_result = self.env['committee.log'].search([(self.env.uid,'in',committee_users.user_id)])
            if (len(is_committee_did_approve) > 0):

                raise Warning(_('you already confirm this order'))
            else:
                self.committee.create({'user_id': self.env.uid ,'po_id':self.id})

                committee_users = self.env['res.users'].search([('groups_id.name','=','committee')])
                committee_users_did_confirm = self.env['committee.log'].search([('po_id','=',self.id),('po_confirm','=',True)])
                if (len(committee_users_did_confirm) > len(committee_users)/2):
                    committee_users_did_confirm.unlink()
                    return super(PurchaseOrder, self).button_confirm()

                #else:
                    #raise Warning(_('waiting other committee to confirm this order'))
        else:
            raise Warning(_('you are not allowed to confirm this order'))


    @api.multi
    def button_cancel(self):
        if(self.amount_total > self.env.user.company_id.currency_id.compute(self.company_id.po_level_three_max_amount, self.currency_id)):
            is_committee_did_cancel = self.env['committee.log'].search([('user_id','=',self.env.uid),('po_id','=',self.id),('po_cancel','=',True)])
            if (len(is_committee_did_cancel)>0):
                raise Warning(_('you already cancel this order'))
            else:
                self.committee.create({'user_id': self.env.uid ,'po_id':self.id , 'po_confirm':False,'po_cancel':True})
                committee_users = self.env['res.users'].search([('groups_id.name','=','committee')])
                committees_did_cancel = self.env['committee.log'].search([('po_id','=',self.id),('po_cancel','=',True)])
                if (len(committees_did_cancel) > len(committee_users)/2):
                    committees_did_cancel.unlink()
                    return super(PurchaseOrder, self).button_cancel()

                #else:
                    #raise Warning(_('waiting other committee to cancel the order'))
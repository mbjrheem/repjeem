__author__ = 'Rheem'
from openerp import *
from openerp import _
from openerp.exceptions import Warning

class MbrHrExpense(models.Model):
    _name = "hr.expense"
    _inherit = ['hr.expense']

    state = fields.Selection([('draft', 'To Submit'),
                              ('submit', 'Submitted'),
                              ('confirm', 'Confirmed'),
                              ('approve', 'Approved'),
                              ('post', 'Waiting Payment'),
                              ('done', 'Paid'),
                              ('cancel', 'Refused')
                              ], string='Status', index=True, readonly=True, track_visibility='onchange', copy=False, default='draft', required=True,
        help='When the expense request is created the status is \'To Submit\'.\n It is submitted by the employee and request is sent to manager, the status is \'Submitted\'.\
        \nIf the manager approve it, the status is \'Approved\'.\n If the accountant genrate the accounting entries for the expense request, the status is \'Waiting Payment\'.')


    @api.multi
    def approve_expenses(self):


        #raise Exception(self.env.user.company_ids.id)
        if ((self.company_id in self.env.user.company_ids) and self.user_has_groups('base.group_hr_manager')):

            self.write({'state': 'approve'})
            accounting_manager_group = self.env['res.groups'].search(
                [('name', '=', 'Adviser'), ('category_id.name', '=', 'Accounting & Finance')])


            users_of_accounting_manager = self.env['res.users'].search([('groups_id', '=', accounting_manager_group.id)])
            body = (_("There is an Expense with name %s has been approved and waiting for payment.<br/><ul class=o_timeline_tracking_value_list></ul>") % (self.name))
            self.message_post(body=body, partner_ids=[user.partner_id.id for user in users_of_accounting_manager])

            #pass
            #body = (_("Your Expense %s has been confirmed.<br/><ul class=o_timeline_tracking_value_list></ul>") % (self.name))
        else:
            raise Warning(_('you are not allowed to Approve this Expense'))
        #raise Exception(hr_manager_users)


    @api.multi
    def confirm_expenses(self):
        emp_direct_manager = self.employee_id.parent_id.user_id

        if (emp_direct_manager == self.env.user or \
            (self.employee_id.user_id == self.env.user and self.user_has_groups('mbr_expense.group_hr_expesne_direct_manager'))):
            #raise Exception('you can confirm :) ')
            self.write({'state': 'confirm'})
            body = (_("There is an Expense with name %s has been confirmed and waiting for your approval.<br/><ul class=o_timeline_tracking_value_list></ul>") % (self.name))
            emp_body = (_("Your Expense %s has been confirmed.<br/><ul class=o_timeline_tracking_value_list></ul>") % (self.name))
            hr_manager_group = self.env['res.groups'].search([('name','=','Manager'),('category_id.name','=','Human Resources')])
            company_of_employee = self.employee_id.user_id.company_id.id
            companys_of_current_user = self.env.user.company_ids
            users_of_hr_manager = self.env['res.users'].search([('groups_id','=',hr_manager_group.id),\
                                    ('company_ids.id','=',company_of_employee)])

            #raise Exception(users_of_hr_manager)
            self.message_post(body=body, partner_ids= [user.partner_id.id for user in users_of_hr_manager])
            self.message_post(body=emp_body, partner_ids=[self.employee_id.parent_id])
        else:
            raise Warning(_('Only the direct manager of this employee can confirm this expense!'))
                # raise Exception(result_msg)
            #users_of_hr_manager_comp_fiter =  self.env['res.users'].search([(company_of_employee,'in',users_of_hr_manager.)])
            #(company_of_employee,'in',companys_of_current_user)



        #self.write({'state': 'confirm'})
        '''
        if self.employee_id.user_id:
            body = (_("There is Expense with name %s has been confirmed and waiting for your approval.<br/><ul class=o_timeline_tracking_value_list></ul>") % (self.name))
            emp_body = (_("Your Expense %s has been confirmed and waiting for Admin approval.<br/><ul class=o_timeline_tracking_value_list></ul>") % (self.name))
            hr_manager_users = self.env['res.users'].search([('groups_id.name','=','Manager'),('groups_id.category_id.name','=','Human Resources')])
                #self.message_post(body=body, partner_ids=[hr_manager_users])
            self.message_post(body=emp_body, partner_ids=[self.employee_id.user_id.partner_id.id])
            for user in hr_manager_users:
                #raise Exception(type(user.partner_id.id))
                self.message_post(body=body, partner_ids=[user.partner_id.id])
                #raise Exception(result_msg)
        '''




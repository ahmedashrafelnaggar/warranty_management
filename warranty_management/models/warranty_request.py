from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta

class WarrantyRequest(models.Model):
    _name = 'warranty.request'
    _description = 'Warranty Request'

    request_number = fields.Char(string='Request Number',readonly=True, default=lambda self: self._generate_request_number())
    customer_id = fields.Many2one('res.partner', string='Customer',required=True)
    product_id = fields.Many2one('product.product', string='Product',required=True)
    purchase_date = fields.Date(string='Purchase Date',required=True)
    warranty_period = fields.Integer(string='Warranty Period',required=True)
    issue_description = fields.Text(string='Issue Description')
    request_status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed')],
        string='Request Status', default='new')
    approval_date = fields.Date(string='Approval Date',readonly=True)
    repair_cost = fields.Float(string='Repair Cost')
    notes = fields.Text(string='Notes')
    is_warranty_valid = fields.Boolean(string='Is Warranty Valid', compute='_compute_is_warranty_valid',store=True)

    @api.depends('purchase_date', 'warranty_period')
    def _compute_is_warranty_valid(self):
        today = date.today()
        for record in self:
            if record.purchase_date:
                purchase_date = fields.Date.from_string(record.purchase_date)
                expiry_date = purchase_date + relativedelta(months=record.warranty_period)
                record.is_warranty_valid = today <= expiry_date
            else:
                record.is_warranty_valid = False

    @api.model
    def _generate_request_number(self):
        today = datetime.today()
        date_str = today.strftime('%d-%m-%Y')
        # Fetch the next sequence number
        sequence_number = self.env['ir.sequence'].next_by_code('warranty.request.sequence') or '0001'
        return f'WRQ-{date_str}-{sequence_number.zfill(4)}'  # Ensure the sequence number is zero-padded to 4 digits

    @api.constrains('warranty_period')
    def _check_warranty_period(self):
        for record in self:
            if record.warranty_period <= 0:
                raise ValidationError("Warranty Period must be greater than 0.")

    @api.constrains('purchase_date')
    def _check_purchase_date(self):
        for record in self:
            if record.purchase_date > fields.Date.today():
                raise ValidationError("Purchase Date cannot be in the future.")

    def action_new(self):
        for rec in self:
            rec.request_status = 'new'

    def action_in_progress(self):
        for rec in self:
            rec.request_status = 'in_progress'

    def approve_request(self):
        for record in self:
            record.request_status = 'approved'
            record.approval_date = date.today()

        # this method of server action or any method in state field

    def action_rejected(self):
        for rec in self:
            rec.request_status = 'rejected'

    def action_completed(self):
        for rec in self:
            rec.request_status = 'completed'

    @api.onchange('request_status')
    def _onchange_request_status(self):
        today = date.today()
        if self.request_status == 'approved' and not self.approval_date:
            self.approval_date = today




    # @api.model
    # def create(self, vals):
    #     if vals.get('request_status') == 'approved' and not vals.get('approval_date'):
    #         vals['approval_date'] = date.today()
    #     return super(WarrantyRequest, self).create(vals)
    #
    # def write(self, vals):
    #     if 'request_status' in vals and vals['request_status'] == 'approved' and not self.approval_date:
    #         vals['approval_date'] = date.today()
    #     return super(WarrantyRequest, self).write(vals)


    # @api.depends('purchase_date', 'warranty_period')
    # def _compute_is_warranty_valid(self):
    #     for record in self:
    #         if record.purchase_date:
    #             end_date = record.purchase_date + relativedelta(months=record.warranty_period)
    #             record.is_warranty_valid = fields.Date.today() <= end_date
    #         else:
    #             record.is_warranty_valid = False
    #
    # @api.constrains('warranty_period')
    # def _check_warranty_period(self):
    #     for record in self:
    #         if record.warranty_period <= 0:
    #             raise ValidationError("Warranty period must be greater than 0.")
# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountAccountCategory(models.Model):
    _name = "account.account.category"
    _description = "Account Category"

    name = fields.Char(string='Account Category', required=True, translate=True)
    note = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', required=True, readonly=True, default=lambda self: self.env.company)


class AccountAccount(models.Model):
    _inherit = 'account.account'
    _parent_name = "parent_id"
    _parent_store = True

    parent_id = fields.Many2one('account.account', 'Parent Account', index=True, ondelete='cascade', check_company=True)
    child_ids = fields.One2many('account.account', 'parent_id', 'Contains')
    parent_path = fields.Char(index=True)

    account_category = fields.Many2one('account.account.category', string='Account Category', required=True)
    balance_direction = fields.Selection([
        ('debit', 'Debit'),
        ('credit', 'Credit')], string='Balance direction',
        default='debit')

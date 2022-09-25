# -*- coding: utf-8 -*-
from odoo import api, fields, models


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

    level_1_id = fields.Many2one('account.account', 'Level 1 Account', compute="_compute_level_1", store=True, readonly=True)

    bend = fields.Boolean(string='Bend', default=False)

    account_category = fields.Many2one('account.account.category', string='Account Category')
    balance_direction = fields.Selection([
        ('debit', 'Debit'),
        ('credit', 'Credit')], string='Balance direction',
        default='debit')

    @api.depends('parent_id', 'parent_path', 'company_id')
    def _compute_level_1(self):
        for record in self:
            if not record.parent_id:
                record.level_1_id = record.id
            elif record.parent_path.count('/') == 2:
                record.level_1_id = record.parent_id
            else:
                top_id = record.parent_path.split('/')[0]
                record.level_1_id = top_id

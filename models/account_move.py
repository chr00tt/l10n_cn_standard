# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    account_id = fields.Many2one(
        domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False),('bend', '=', True)]",
        )

    parent_account = fields.Many2one(string='Parent Account', related='account_id.parent_id', store=True)
    level_1_account = fields.Many2one(string='Level 1 Account', related='account_id.level_1_id', store=True)
    
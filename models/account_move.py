# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    parent_account = fields.Many2one(string='Parent Account', related='account_id.parent_id', store=True)
    
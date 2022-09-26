# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('reviewed', 'Reviewed'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ])

    def _review(self):
        if self.state == 'reviewed':
            raise UserError(_('The entry %s (id %s) is already reviewed.') % (self.name, self.id))
        if not self.line_ids.filtered(lambda line: not line.display_type):
            raise UserError(_('You need to add a line before reviewing.'))

        self.write({
            'state': 'reviewed'
        })

    def action_review(self):
        self._review()


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # 只允许使用末级科目
    account_id = fields.Many2one(
        domain="[('deprecated', '=', False), ('company_id', '=', 'company_id'),('is_off_balance', '=', False),('bend', '=', True)]",
        )

    # 按上级科目分组汇总
    parent_account = fields.Many2one(string='Parent Account', related='account_id.parent_id', store=True)
    # 按一级科目分组汇总
    level_1_account = fields.Many2one(string='Level 1 Account', related='account_id.level_1_id', store=True)
    
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountCategoryTemplate(models.Model):
    _name = "account.category.template"
    _description = 'Template for Account Categories'
    
    name = fields.Char(required=True)
    chart_template_id = fields.Many2one('account.chart.template', string='Chart Template', required=True)


class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"
    _parent_name = "parent_id"
    _parent_store = True

    parent_id = fields.Many2one('account.account.template', 'Parent Account', index=True, ondelete='cascade', check_company=True)
    child_ids = fields.One2many('account.account.template', 'parent_id', 'Contains')
    parent_path = fields.Char(index=True)
    
    bend = fields.Boolean(string='Bend', default=False)

    account_category = fields.Many2one('account.category.template', string='Account Category')
    balance_direction = fields.Selection([
        ('debit', 'Debit'),
        ('credit', 'Credit')], string='Balance direction',
        default='debit')


class AccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _create_bank_journals(self, company, acc_template_ref):
        '''
        This function creates bank journals and their account for each line
        data returned by the function _get_default_bank_journals_data.

        :param company: the company for which the wizard is running.
        :param acc_template_ref: the dictionary containing the mapping between the ids of account templates and the ids
            of the accounts that have been generated from them.
        '''
        self.ensure_one()
        bank_journals = self.env['account.journal']
        # Create the journals that will trigger the account.account creation
        for acc in self._get_default_bank_journals_data():
            vals = {
                'name': acc['acc_name'],
                'type': acc['account_type'],
                'company_id': company.id,
                'currency_id': acc.get('currency_id', self.env['res.currency']).id,
                'sequence': 10,
            }
            # 允许会计制度设置生成的日记帐科目
            if acc['default_account_id']:
                vals['default_account_id'] = acc_template_ref[acc['default_account_id']]
                # 未收账款和未付款账户不用单独的中间科目
                vals['payment_debit_account_id'] = acc_template_ref[acc['default_account_id']]
                vals['payment_credit_account_id'] = acc_template_ref[acc['default_account_id']]
            bank_journals += self.env['account.journal'].create(vals)

        return bank_journals

    @api.model
    def _get_default_bank_journals_data(self):
        if not self == self.env.ref('l10n_cn_standard.l10n_chart_china_standard_business'):
            return super(AccountChartTemplate, self)._get_default_bank_journals_data()

        return [
            {
                'acc_name': _('Cash'), 'account_type': 'cash',
                'default_account_id': self.env.ref('l10n_cn_standard.account_1001').id
            },
            {
                'acc_name': _('Bank'), 'account_type': 'bank',
                'default_account_id': self.env.ref('l10n_cn_standard.account_1002').id,
            },
        ]

    def generate_categories(self, company):
        self.ensure_one()
        category_templates = self.env['account.category.template'].search([('chart_template_id', '=', self.id)])
        template_vals = []
        for category_template in category_templates:
            vals = {
                'name': category_template.name,
                'company_id': company.id,
            }
            template_vals.append((category_template, vals))
        groups = self._create_records_with_xmlid('account.account.category', template_vals, company)

        category_template_ref = {}
        for template, group in zip(category_templates, groups):
            category_template_ref[template.id] = group.id
        return category_template_ref

    def _get_account_vals(self, company, account_template, code_acc, tax_template_ref, category_template_ref):
        val = super(AccountChartTemplate, self)._get_account_vals(company, account_template, code_acc, tax_template_ref)
        # # 处理添加的字段
        val['bend'] = account_template.bend
        val['account_category'] = account_template.account_category and category_template_ref[account_template.account_category.id] or False
        val['balance_direction'] = account_template.balance_direction
        return val

    def generate_account(self, tax_template_ref, acc_template_ref, code_digits, company):
        category_template_ref = self.generate_categories(company)

        self.ensure_one()
        account_tmpl_obj = self.env['account.account.template']
        acc_template = account_tmpl_obj.search([('nocreate', '!=', True), ('chart_template_id', '=', self.id)], order='id')
        template_vals = []
        for account_template in acc_template:
            # 科目代码不需要补齐到6位
            code_acc = account_template.code or ''
            vals = self._get_account_vals(company, account_template, code_acc, tax_template_ref, category_template_ref)
            template_vals.append((account_template, vals))
        accounts = self._create_records_with_xmlid('account.account', template_vals, company)
        for template, account in zip(acc_template, accounts):
            acc_template_ref[template.id] = account.id

        # 更新 parent_id
        for template, account in zip(acc_template, accounts):
            if template.parent_id:
                account.update({'parent_id': acc_template_ref[template.parent_id.id]})

        return acc_template_ref

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 企业会计准则',
    'version': '2.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': ['lvxin@gmail.co', 'oldrev@gmail.co', 'ccdos@intoerp.com', 'jeff@osbzr.com', 'jeffery9@gmail.com', '1217875253@qq.com'],

    'website': 'https://github.com/chr00tt/l10n_cn_standard',
    'description': """
Including the following data in the Accounting Standards for Business Enterprises
包含企业会计准则以下数据

* Chart of Accounts
* 科目表模板

* Account templates
* 科目模板

* Tax templates
* 税金模板

    """,
    'depends': ['l10n_cn'],
    'data': [
        'data/l10n_cn_standard.xml',
        'data/account.account.template.csv',
        'data/account_tax_template_data.xml',
        'data/l10n_cn_standard_post.xml',
    ],
    'license': 'LGPL-3',
}

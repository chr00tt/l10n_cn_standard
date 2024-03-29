# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 企业会计准则',
    'version': '2.0',
    'author': "He Jian",
    'category': 'Accounting/Localizations/Account Charts',
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
    'depends': [
        'account',
        "l10n_multilang",
    ],
    'data': [
        'data/l10n_cn_standard.xml',
        'data/account.account.template.csv',
        'data/l10n_cn_standard_post.xml',
    ],
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': '中国 - 企业会计准则',
    'website': 'https://github.com/chr00tt/l10n_cn_standard',
    'author': "He Jian",
    'category': 'Accounting/Localizations/Account Charts',
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

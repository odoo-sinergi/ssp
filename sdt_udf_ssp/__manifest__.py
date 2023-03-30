# -*- coding: utf-8 -*-
{
    'name': "SDT UDF SSP",

    'summary': """
        SDT UDF SSP """,

    'description': """
        STD UDF all module by PT. Sinergi Data Totalindo
    """,

    'author': "Sinergi Data Totalindo, PT",
    'website': "http://www.sinergidata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'account',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/user_groups.xml',
        # 'views/purchase_order.xml',
        # 'views/sale_order.xml',
        # 'views/account_payment.xml',
        # 'views/res_partner.xml',
        # 'views/project.xml',
        # 'views/product.xml',
        # 'views/mrp_bom.xml',
        'views/stock.xml',
        'views/account_move.xml',
        # 'views/account_analytic_account.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
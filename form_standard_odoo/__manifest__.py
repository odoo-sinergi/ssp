# -*- coding: utf-8 -*-
{
    'name': "SDT Standard Form",

    'summary': """
        Form Standard""",

    'description': """
        Form Standard
    """,

    'author': "Sinergi Data Totalindo, PT",
    'website': "http://www.sinergidata.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'account',
                'sale',
                'purchase',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        # 'report/sdt_standard_good_receipt.xml',
        # 'report/sdt_standard_inventory_transfer.xml',
        # 'report/sdt_standard_payment_receipt.xml',
        'report/template.xml',
        'wizard/sdt_payment.xml',
        'views/account_payment.xml',
        # report
        'report/sdt_standard_purchase_order.xml',
        'report/sdt_standard_sales_invoice.xml',
        'report/sdt_standard_form_voucher.xml',
        'report/sdt_standard_delivery_order.xml',
        'report/sdt_standard_cash_advance.xml',
    ],
    # only loaded in demonstration mode
}
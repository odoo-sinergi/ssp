# -*- coding: utf-8 -*-
{
    'name': "SDT UDF Res Partner SSP",

    'summary': """
        SDT UDF Res Partner SSP """,

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
        'contacts',
        # 'account',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/user_groups.xml',
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
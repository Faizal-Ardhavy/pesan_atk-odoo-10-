# -*- coding: utf-8 -*-
{
    'name': "Pemesanan ATK",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/report_view.xml',
        'report/print_sesi.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/pemesanan.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
        'wizard/reject_wizard.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
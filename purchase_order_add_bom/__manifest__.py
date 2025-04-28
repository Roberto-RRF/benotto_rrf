{
    'name': 'Purchase Order Add Bill of Materials',
    'version': '1.0',
    'author':'ANFEPI: Roberto Requejo Fernández',
    'depends': ['purchase'],
    'description': """
    """,
    'data': [
        'views/purchase_order_views.xml',
        'wizard/purchase_order_bom_wizard_view.xml',
        'security/ir.model.access.csv'
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    "license": "AGPL-3",
}
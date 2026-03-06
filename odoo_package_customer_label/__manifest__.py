{
    'name': 'Package Label with Customer',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Customer details in ZPL label on Odoo',
    'description': """
        Module:
        - Computed field partner_id στο stock.quant.package
        - Updated ZPL label template with Customer details
    """,
    'author': 'co-ux99',
    'website': 'https://www.illusioweb.com',
    'depends': [
        'stock',
        'delivery',
    ],
    'data': [
        'views/package_label_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
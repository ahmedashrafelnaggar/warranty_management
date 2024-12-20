{
    "name": "Warranty Management",
    "summary": "Manage warranty requests for TechMart",
    "author": "TechMart",
    # "depends": ["base", "sales", "product"],
    "depends": ["base", "sale_management"],
    'version': '16.0.0.1',
    'license': 'OPL-1',
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/warranty_request_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
# -*- coding: utf-8 -*-
{
    'name': 'Website Guest Price Hide',
    'category': 'Website',
    'summary': 'Website Guest Price Hide',
    'version': '1.1',
    'license': 'OPL-1',
    'author': 'Atharva System',
    'website': 'https://www.atharvasystem.com',
    'support': 'support@atharvasystem.com',
    'description': """
    """,
    'depends': ['atharva_theme_general','crm'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': ['/website_guest_price_hide/static/src/xml/*.xml'],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}

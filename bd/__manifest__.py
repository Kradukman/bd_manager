# -*- encoding: utf-8 -*-
{
    'name': 'bd',
    'version': '13.0',
    'description': """Manage bd""",

    'depends': [
        'base',
        'contacts',
    ],
    'data': [
        # assets
        # models

        # fields
        # actions
        # reports
        # security
        'security/ir.model.access.csv',
        # views
        'views/bd_module.xml',
        'views/bd.xml',
        'views/author.xml',
        'views/publisher.xml',
        'views/serie.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
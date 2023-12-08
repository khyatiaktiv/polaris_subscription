# -*- coding: utf-8 -*-
# © 2018-Today Aktiv Software (http://aktivsoftware.com).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Kanban",
    'summary': """
       """,
    'description': """
    """,
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'category': 'MRP',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        "base", "base_setup",
        'kanban_for_manufacturing'],

    'data': [
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kanban_scan/static/src/js/kanban_reordering.js',
            'kanban_scan/static/src/less/kfm_krr_barcode.less',
            'kanban_scan/static/src/xml/*'
        ],
        # 'web.assets_qweb': [
        #     'kanban_scan/static/src/xml/*',
        #     ],
    }
}

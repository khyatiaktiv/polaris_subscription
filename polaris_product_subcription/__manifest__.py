# -*- coding: utf-8 -*-

{
    "name": "Polaris | Product Subscription",
    "summary": """Product Subscription""",
    "description": """
    Product Subscription with API key
    """,
    "author": "",
    "website": "",
    "category": "Sale/Sale",
    "license": "LGPL-3",
    "version": "16.0.1.0.0",
    "depends": ["sale_subscription"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/product_views.xml",
    ],
    "application": True,
    "auto_install": False,
}

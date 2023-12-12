# -*- coding: utf-8 -*-

{
    "name": "Polaris || Product Subscription",
    "summary": """Product Subscription""",
    "description": """
    Product Subscription with API key
    """,
    "author": "",
    "website": "",
    "category": "Sale/Sale",
    "license": "LGPL-3",
    "version": "17.0.1.0.0",
    "depends": ["sale_subscription", "account"],
    "data": [
        "security/ir.model.access.csv",
        "data/invoice_email_template.xml",
        "views/sale_order_views.xml",
        "views/product_views.xml",
        "views/sale_order_api_key_history.xml",
        "views/subscription_portal_templates.xml",
        "report/subscription_api_report.xml"
    ],
    "application": True,
    "auto_install": False,
}

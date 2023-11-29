# -*- coding: utf-8 -*-

import requests
from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def connect_to_odoo_server(self):
        endpoint = "http://192.168.1.113:8016/api_validation"  # Static URL
        params = self.env["ir.config_parameter"].sudo()
        payload = {
            "client_url": params.get_param("web.base.url"),
            "expiration_date": params.get_param(
                "polaris_product_subscription.x_module_expiration_date"
            ),
            "api_key": params.get_param(
                "polaris_product_subscription.x_module_api_key"
            ),
            "module_name": "x_module",
        }
        try:
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
            )
            print("\n\nresponse", response)
            try:
                response_data = response.json()
                print("\n\nresponse_data", response_data)
                return response_data
            except Exception as e:
                return e
        except KeyError:
            print("The 'result' key is missing in the JSON response.")
            return None

# -*- coding: utf-8 -*-

import requests
from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def connect_to_odoo_server_polaris_custom_module_code(self):
        """
        Cron job method to check for validation of api key
        """
        endpoint = "http://192.168.1.113:8016/api_validation"  # Static URL
        params = self.env["ir.config_parameter"].sudo()
        payload = {
            "client_domain": params.get_param("web.base.url"),
            "api_key": params.get_param(
                "polaris_custom_module_code.polaris_custom_module_code_api_key"
            ),
            "module_name": "polaris_custom_module_code",
        }
        try:
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
            )
            try:
                response_data = response.json()
                print("\n\nresponse_data>>>>>>>>", response_data["result"])
                return response_data
            except Exception as e:
                return e
        except KeyError:
            print("The 'result' key is missing in the JSON response.")
            return None

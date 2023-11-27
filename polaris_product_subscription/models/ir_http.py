# -*- coding: utf-8 -*-

import json
import requests
from odoo import models


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    # def webclient_rendering_context(self):
    #     """ Overrides community to prevent unnecessary load_menus request """
    #     return {
    #         'session_info': self.session_info(),
    #     }
    #
    # def session_info(self):
    #     result = super(Http, self).session_info()
    #     print("\n\n\n>>>>>>>result>>>>>", result)
    #     return result
    
    def connect_to_odoo_server(path, parameters):
        endpoint = 'http://192.168.1.113:8016/api_validation'  # Update with your Odoo instance URL
        payload = {
            'params': parameters,
        }
        try:
            response = requests.post(endpoint,
                                     headers={'Content-Type': 'application/json'},
                                     json=payload)
            try:
                response_data = response.json()
                return response_data
            except Exception as e:
                return e
        except KeyError:
            print("The 'result' key is missing in the JSON response.")
            return None


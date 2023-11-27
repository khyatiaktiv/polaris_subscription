# -*- coding: utf-8 -*-


from odoo import http
import json


class OdooAPIController(http.Controller):
    @http.route('/api_validation', type='json', auth='public')
    def api_validation(self, **kw):
        # Access the request parameters
        parameters = json.loads(http.request.httprequest.data)
        # Process the API request and return the response
        print("\n\ncalllllllllllllllllllllll", )
        response = {
            'status': 'success',
            'message': 'API request received without authentication',
            'data': {
                'parameters': parameters
            }
        }
        return response
    
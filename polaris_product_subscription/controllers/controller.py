# -*- coding: utf-8 -*-
import datetime
import json

from odoo import http
from odoo.http import request


class OdooAPIController(http.Controller):
    @http.route("/api_validation", type="json", auth="public")
    def api_validation(self, **kw):
        # Access the request parameters
        data = json.loads(http.request.httprequest.data)
        # Process the API request and return the response
        valid_api_key = request.env["sale.order.line.api.key"].search(
            [
                ("api_key", "=", data["api_key"]),
                ("technical_name", "=", data["module_name"]),
            ]
        )
        if valid_api_key:
            if valid_api_key.status == "start":
                valid_api_key.status = "inprogress"
            if valid_api_key.status == "inprogress":
                if not valid_api_key.client_domain:
                    valid_api_key.client_domain = data["client_domain"]
                if valid_api_key.client_domain != data["client_domain"]:
                    return {
                        "status": "invalid_key",
                        "message": "Invalid Api Key",
                    }
                if valid_api_key.key_expiration_date <= datetime.date.today():
                    valid_api_key.status = "stop"
                return {"status": "valid_key", "message": "Valid Api Key"}
            if valid_api_key.status == "stop":
                return {
                    "status": "expired_key",
                    "message": "API Key Has expired",
                }
        else:
            return {"status": "invalid_key", "message": "Invalid Api Key"}

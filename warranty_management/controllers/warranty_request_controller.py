import requests
from odoo import http
from odoo import fields
from odoo.http import request
import json
from odoo.exceptions import UserError


class LoginController(http.Controller):
    @http.route("/api/login", methods=["POST"], type="json", auth="none", csrf=False)
    def login(self, login, password):

        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = base_url + '/web/session/authenticate'
        headers = {
            'Content-Type': 'application/json', }

        data = {
            "params": {
                "db": request.db,
                "login": login,
                "password": password,
            }

        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            try:
                response_body = response.json()
                cookies = response.cookies.get_dict()
                session_id = cookies.get('session_id', False)
                if session_id and response_body['result']:
                    return {'session_id': session_id}
            except Exception as e:
                return {
                    'success': False,
                    'message': 'Could Not Perform Login',
                    'response': response}

    @http.route("/api/create/warranty/request", type="json", auth="public", methods=["POST"])
    def create_warranty_request(self, **kw):
        try:
            # Extracting data from the request
            customer_id = kw.get('customer_id')
            product_id = kw.get('product_id')
            purchase_date = kw.get('purchase_date')
            warranty_period = kw.get('warranty_period')
            issue_description = kw.get('issue_description')

            # Input validation

            if not customer_id:
                return {'error': 'Missing required field: customer_id', 'code': 400}
            if not product_id:
                return {'error': 'Missing required field: product_id', 'code': 400}
            if not purchase_date:
                return {'error': 'Missing required field: purchase_date', 'code': 400}
            if not warranty_period:
                return {'error': 'Missing required field: warranty_period', 'code': 400}
            if not issue_description:
                return {'error': 'Missing required field: issue_description', 'code': 400}

            customer = request.env['res.partner'].sudo().browse(product_id)
            product = request.env['product.product'].sudo().browse(product_id)

            # Create a new warranty request
            warranty_request = request.env['warranty.request'].sudo().create({
                'customer_id': customer.id,
                'product_id': product.id,
                'purchase_date': purchase_date,
                'warranty_period': warranty_period,
                'issue_description': issue_description,
                'request_status': 'new',  # Default status
            })

            # Prepare the response
            return {
                'success': True,
                'request_number': warranty_request.request_number,
                'warranty_request': warranty_request.id,
            }

        except Exception as e:
            # Handle unexpected errors
            return {'success': False, 'message': f'Error: {str(e)}'}
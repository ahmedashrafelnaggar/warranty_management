# -*- coding: utf-8 -*-
# from odoo import http


# class WarrantyManagement(http.Controller):
#     @http.route('/warranty_management/warranty_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/warranty_management/warranty_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('warranty_management.listing', {
#             'root': '/warranty_management/warranty_management',
#             'objects': http.request.env['warranty_management.warranty_management'].search([]),
#         })

#     @http.route('/warranty_management/warranty_management/objects/<model("warranty_management.warranty_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('warranty_management.object', {
#             'object': obj
#         })

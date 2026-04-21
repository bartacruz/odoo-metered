# from odoo import http


# class ElectricUtility(http.Controller):
#     @http.route('/electric_utility/electric_utility', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/electric_utility/electric_utility/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('electric_utility.listing', {
#             'root': '/electric_utility/electric_utility',
#             'objects': http.request.env['electric_utility.electric_utility'].search([]),
#         })

#     @http.route('/electric_utility/electric_utility/objects/<model("electric_utility.electric_utility"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('electric_utility.object', {
#             'object': obj
#         })

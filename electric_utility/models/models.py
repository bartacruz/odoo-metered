# from odoo import models, fields, api


# class electric_utility(models.Model):
#     _name = 'electric_utility.electric_utility'
#     _description = 'electric_utility.electric_utility'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

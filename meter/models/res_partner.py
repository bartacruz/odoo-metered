from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    meter_ids = fields.One2many("meter", "partner_id")

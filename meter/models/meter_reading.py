from odoo import models, fields


class MeterReading(models.Model):
    _name = "meter.reading"
    _description = "a meter reading"
    _order = "date desc"

    meter_id = fields.Many2one("meter")
    date = fields.Datetime()
    value = fields.Integer(default=0)

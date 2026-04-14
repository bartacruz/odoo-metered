from odoo import models, fields, api


class Meter(models.Model):
    _name = "meter"
    _description = "a meter that has periodic readings with values"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char()
    state = fields.Selection(
        [
            ("requested", "Requested"),
            ("active", "Active"),
            ("cancelled", "Cancelled"),
        ],
        default="requested",
        tracking=True,
    )

    reading_ids = fields.One2many("meter.reading", "meter_id")
    reading_count = fields.Integer(compute="_compute_readings", store=True)
    last_reading_id = fields.Many2one(
        "meter.reading", compute="_compute_readings", store=True
    )
    last_reading_value = fields.Integer(related="last_reading_id.value")
    last_reading_date = fields.Datetime(related="last_reading_id.date")
    last_period_days = fields.Integer(compute="_compute_readings", store=True)
    last_period_value = fields.Integer(compute="_compute_readings", store=True)

    @api.depends("reading_ids", "reading_ids.value", "reading_ids.date")
    def _compute_readings(self):
        for record in self:
            reading_count = len(record.reading_ids)
            record.reading_count = reading_count
            if reading_count > 0:
                record.last_reading_id = record.reading_ids[0]
            if reading_count < 2:
                record.last_period_days = 0
                record.last_period_value = 0
            else:
                record.last_period_days = (
                    record.reading_ids[0].date - record.reading_ids[1].date
                ).days
                record.last_period_value = (
                    record.reading_ids[0].value - record.reading_ids[1].value
                )

    def total_period_values(self):
        val = sum(self.mapped("last_period_value"))
        return val

    def action_open_readings(self):
        self.ensure_one()
        action = self.env.ref("meter.action_meter_reading").read()[0]
        action["context"] = {"default_meter_id": self.id}
        action["domain"] = [("id", "in", self.reading_ids.ids)]
        return action

from odoo import _, models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Contract(models.Model):
    _inherit = "contract.contract"

    meter_ids = fields.Many2many("meter")
    meter_count = fields.Integer(compute="_compute_meter_count", store=True)
    meters_ready_to_invoice = fields.Boolean(
        compute="_compute_meters_ready_to_invoice", store=True
    )

    @api.depends("meter_ids")
    def _compute_meter_count(self):
        for record in self:
            record.meter_count = len(record.meter_ids)
            if record.active:
                to_add = record.meter_ids.filtered(lambda m: m.contract_id != record)
                for meter in to_add:
                    line_values = record.contract_line_ids._get_meter_line_values(meter)
                    record.contract_line_ids = [(0, 0, line_values)]
                _logger.info(
                    "_compute_meter_count %s %s %s",
                    to_add,
                    record,
                    record.contract_line_ids,
                )

    @api.depends("meter_ids.ready_to_invoice")
    def _compute_meters_ready_to_invoice(self):
        for record in self:
            record.meters_ready_to_invoice = all(
                m.ready_to_invoice for m in record.meter_ids
            )

    def recurring_create_invoice(self):
        today = fields.Date.context_today(self)
        not_ready = self.search(
            [
                ("active", "=", True),
                ("recurring_next_date", "<=", today),
                ("meters_ready_to_invoice", "=", False),
            ],
            limit=1,
        )

        if not_ready:
            raise UserError(_("Meters are not ready to invoice"))
        return super(Contract, self).recurring_create_invoice()

    @api.model
    def cron_recurring_create_invoice(self):
        today = fields.Date.context_today(self)
        not_ready = self.search(
            [
                ("state", "=", "open"),
                ("recurring_next_date", "<=", today),
                ("meter_ids.ready_to_invoice", "=", False),
            ],
            limit=1,
        )

        if not_ready:
            _logger.warning(
                _("Create recurring invoices stopped. Some meters are not ready")
            )
            return
        return super(Contract, self).cron_recurring_create_invoice()

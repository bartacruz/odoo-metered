from odoo import _, models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class Meter(models.Model):
    _inherit = "meter"

    # TODO: Add related to contract_line_id?
    contract_ids = fields.Many2many(
        "contract.contract",
        string="Contracts",
        compute="_compute_contract_line",
        store=True,
    )
    contracts_count = fields.Integer(compute="_compute_contract_line", store=True)
    contract_line_ids = fields.One2many(
        "contract.line", "meter_id", string="Contract Lines"
    )
    contract_line_id = fields.Many2one(
        "contract.line",
        string="Contract Line",
        compute="_compute_contract_line",
        store=True,
    )
    contract_id = fields.Many2one(
        "contract.contract", string="Contract", related="contract_line_id.contract_id"
    )
    ready_to_invoice = fields.Boolean(compute="_compute_ready_to_invoice", store=True)

    @api.depends("contract_line_ids")
    def _compute_contract_line(self):
        for record in self:
            line = record.contract_line_ids.filtered(lambda cl: cl.contract_id.active)
            if len(line) > 1:
                raise UserError(
                    _(
                        "Configuration Error: meter %s is in more than one active contracts",
                        record.name,
                    )
                )
            record.contract_line_id = line.id
            record.contract_ids = record.contract_line_ids.mapped("contract_id").ids
            _logger.info(
                "_compute_contract_line %s %s %s",
                record,
                record.contract_line_id,
                record.contract_ids,
            )
            record.contracts_count = len(record.contract_ids)

    @api.depends("contract_id", "contract_id.active", "last_reading_date")
    def _compute_ready_to_invoice(self):
        contract_meters = self.filtered(
            lambda r: r.contract_id and r.contract_id.active
        )
        (self - contract_meters).ready_to_invoice = False
        for record in contract_meters:
            last_inv_date = (
                record.contract_id.last_date_invoiced
                or fields.Date.to_date("1900-01-01")
            )
            record.ready_to_invoice = (
                record.last_reading_date
                and record.last_reading_date.date() > last_inv_date
            )

    def total_period_values(self):
        contracts = self.mapped("contract_id")
        if len(contracts) == 0:
            return super().total_period_values()
        if len(contracts) > 1:
            raise UserError(
                _("Configuration Error: meters belong to different contracts")
            )
        to_invoice = self.filtered(lambda m: m.ready_to_invoice)
        if len(to_invoice) < len(self):
            raise UserError(
                _("Meters not ready to invoice: %s", (self - to_invoice).mapped("name"))
            )
        return sum(to_invoice.mapped("last_period_value"))

    def action_open_contracts(self):
        self.ensure_one()
        action = self.env.ref("contract.action_customer_contract").read()[0]
        action["domain"] = [("id", "in", self.contract_ids.ids)]
        return action

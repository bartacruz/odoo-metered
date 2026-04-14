from odoo import models, fields, api


class ContractLine(models.Model):
    _inherit = "contract.line"

    meter_id = fields.Many2one("meter")

    @api.model
    def _get_meter_line_values(self, meter):
        formula = self.env.ref(
            "meter_contract.line_qty_formula_meter", raise_if_not_found=False
        )
        product_id = self.env["product.product"].search(
            [("default_code", "=", "METERED")], limit=1
        )
        line_values = {
            "product_id": product_id.id if product_id else False,
            "meter_id": meter.id,
            "name": f"Meter: {meter.name}",
            "qty_type": "variable",
            "qty_formula_id": formula.id if formula else False,
            "automatic_price": True,
        }
        return line_values

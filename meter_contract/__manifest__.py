{
    "name": "Meter Contract Integration",
    "summary": "Consumption-based invoicing using contracts",
    "author": "Julio Santa Cruz",
    "website": "https://github.com/bartacruz/odoo-metered",
    "license": "AGPL-3",
    "category": "Accounting/Accounting",
    "version": "18.0.0.0.1",
    "installable": True,
    "application": False,
    "depends": ["base", "contract", "contract_variable_quantity", "meter"],
    "data": [
        "data/meter_contract_data.xml",
        "views/contract.xml",
        "views/meter.xml",
    ],
}

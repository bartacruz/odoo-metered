{
    "name": "Meter Management",
    "summary": "Odoo Support for Meter Devices",
    "author": "Julio Santa Cruz",
    "website": "https://github.com/bartacruz/odoo-metered",
    "license": "AGPL-3",
    "category": "Services/Services",
    "version": "18.0.0.0.1",
    "installable": True,
    "application": True,
    # any module necessary for this one to work correctly
    "depends": ["base", "mail"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/meter.xml",
        "views/meter_reading.xml",
        "views/menu.xml",
    ],
}

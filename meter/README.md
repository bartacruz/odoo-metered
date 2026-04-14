# Odoo Support for Meter Devices

This is the core module for meter devices tracking in Odoo. It introduces the fundamental data structures to manage physical measuring devices and their history.

## Features

- Meter Model (`meter`): Define and categorize different types of meters (water, electricity, gas, etc.). Has a phisical location, dated readings, handles preriodical values, etc.
- Meter Readings (`meter.reading`): Track consumption through a dedicated model, maintaining a historical log of all measurements.
- Unit of Measure Support: Compatible with standard Odoo UoM for precise consumption tracking.

## Authors

- [Julio Santa Cruz](https://github.com/bartacruz)

## License

This module is licensed under [AGPL-3.0](../LICENSE).

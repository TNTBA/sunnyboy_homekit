"""Constants for the SMA Sunnyboy Solar integration."""

DOMAIN = "sunnyboy"

# Configuration
CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Default values
DEFAULT_SCAN_INTERVAL = 30  # seconds
DEFAULT_USERNAME = "user"

# Sensor types
SENSOR_TYPES = {
    "current_power": {
        "name": "Current Power",
        "unit": "W",
        "icon": "mdi:solar-power",
        "device_class": "power",
        "state_class": "measurement",
    },
    "daily_energy": {
        "name": "Daily Energy",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
    "total_energy": {
        "name": "Total Energy",
        "unit": "kWh",
        "icon": "mdi:solar-power",
        "device_class": "energy",
        "state_class": "total_increasing",
    },
}

"""Sensor platform for SMA Sunnyboy Solar integration."""
import logging
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, SENSOR_TYPES, CONF_HOST

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up SMA Sunnyboy Solar sensors from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    host = entry.data[CONF_HOST]

    # Create sensor entities
    entities = []
    for sensor_type in SENSOR_TYPES:
        entities.append(SunnyBoySensor(coordinator, host, sensor_type))

    async_add_entities(entities)


class SunnyBoySensor(CoordinatorEntity, SensorEntity):
    """Representation of a SMA Sunnyboy sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        host: str,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._host = host
        self._attr_name = f"Sunnyboy {SENSOR_TYPES[sensor_type]['name']}"
        self._attr_unique_id = f"sunnyboy_{host}_{sensor_type}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_device_class = SENSOR_TYPES[sensor_type].get("device_class")
        self._attr_state_class = SENSOR_TYPES[sensor_type].get("state_class")

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information about this inverter."""
        return {
            "identifiers": {(DOMAIN, self._host)},
            "name": f"Sunnyboy Inverter {self._host}",
            "manufacturer": "SMA",
            "model": "Sunnyboy",
        }

    @property
    def native_value(self) -> Optional[float]:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

"""The SMA Sunnyboy Solar integration."""
import asyncio
import logging
from datetime import timedelta
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from .sunnyboy_api import SunnyBoyAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SMA Sunnyboy Solar from a config entry."""
    host = entry.data[CONF_HOST]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    # Create API client
    api = SunnyBoyAPI(host, username, password, session=async_get_clientsession(hass))

    # Test connection
    try:
        if not await api.test_connection():
            await api.close()
            raise ConfigEntryNotReady(f"Unable to connect to Sunnyboy inverter at {host}")
    except Exception as err:
        await api.close()
        raise ConfigEntryNotReady(f"Error connecting to Sunnyboy inverter: {err}")

    # Create update coordinator
    async def async_update_data() -> Dict[str, Any]:
        """Fetch data from API."""
        try:
            data = await api.get_data()
            if data is None:
                raise UpdateFailed("Failed to fetch data from inverter")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with inverter: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"sunnyboy_{host}",
        update_method=async_update_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator and API
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        # Close API connection
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["api"].close()

    return unload_ok

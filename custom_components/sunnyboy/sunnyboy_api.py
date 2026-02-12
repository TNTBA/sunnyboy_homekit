"""API client for SMA Sunnyboy inverters."""
import asyncio
import logging
from typing import Any, Dict, Optional
import aiohttp
import hashlib
import json

_LOGGER = logging.getLogger(__name__)


class SunnyBoyAPI:
    """API client for SMA Sunnyboy inverters using WebConnect."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """Initialize the API client."""
        self.host = host
        self.username = username
        self.password = password
        self._session = session
        self._owned_session = session is None
        self._sid = None
        self._base_url = f"http://{host}"

    async def _ensure_session(self):
        """Ensure an aiohttp session exists."""
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        """Close the API client and logout."""
        if self._sid:
            await self.logout()
        if self._owned_session and self._session:
            await self._session.close()
            self._session = None

    async def login(self) -> bool:
        """Authenticate with the inverter."""
        await self._ensure_session()
        
        try:
            # Modern SMA inverters use the new API with JSON-RPC
            url = f"{self._base_url}/dyn/login.json"
            
            # Create password hash
            pass_hash = hashlib.md5(self.password.encode()).hexdigest()
            
            payload = {
                "right": self.username,
                "pass": pass_hash
            }
            
            async with self._session.post(url, json=payload, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    self._sid = data.get("result", {}).get("sid")
                    if self._sid:
                        _LOGGER.debug("Successfully logged in to Sunnyboy inverter")
                        return True
                    
            _LOGGER.error("Login failed: No session ID received")
            return False
            
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout connecting to inverter at %s", self.host)
            return False
        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error to inverter: %s", err)
            return False
        except Exception as err:
            _LOGGER.error("Unexpected error during login: %s", err)
            return False

    async def logout(self):
        """Logout from the inverter."""
        if not self._sid:
            return
            
        try:
            url = f"{self._base_url}/dyn/logout.json"
            payload = {"sid": self._sid}
            async with self._session.post(url, json=payload, timeout=5):
                pass
            self._sid = None
        except Exception as err:
            _LOGGER.debug("Error during logout: %s", err)

    async def get_data(self) -> Optional[Dict[str, Any]]:
        """Fetch current data from the inverter."""
        if not self._sid:
            if not await self.login():
                return None
        
        await self._ensure_session()
        
        try:
            # Request current power and energy data
            url = f"{self._base_url}/dyn/getValues.json"
            
            payload = {
                "destDev": [],
                "keys": [
                    "6100_40263F00",  # Current power (W)
                    "6400_00260100",  # Daily yield (Wh)
                    "6400_00260001",  # Total yield (Wh)
                ]
            }
            
            if self._sid:
                payload["sid"] = self._sid
            
            async with self._session.post(url, json=payload, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_values(data)
                elif response.status == 401:
                    # Session expired, try to re-login
                    _LOGGER.debug("Session expired, attempting re-login")
                    self._sid = None
                    if await self.login():
                        return await self.get_data()
                    
            return None
            
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout fetching data from inverter")
            return None
        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error fetching data: %s", err)
            return None
        except Exception as err:
            _LOGGER.error("Unexpected error fetching data: %s", err)
            return None

    def _parse_values(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the values from the inverter response."""
        result = {
            "current_power": 0,
            "daily_energy": 0,
            "total_energy": 0,
        }
        
        try:
            if "result" not in data:
                return result
                
            values = data["result"]
            
            # Extract values from the nested structure
            for key, value_data in values.items():
                if "6100_40263F00" in key:  # Current power
                    val = value_data.get("1", [{}])[0].get("val")
                    if val is not None:
                        result["current_power"] = int(val)
                        
                elif "6400_00260100" in key:  # Daily yield
                    val = value_data.get("1", [{}])[0].get("val")
                    if val is not None:
                        result["daily_energy"] = round(val / 1000, 2)  # Convert Wh to kWh
                        
                elif "6400_00260001" in key:  # Total yield
                    val = value_data.get("1", [{}])[0].get("val")
                    if val is not None:
                        result["total_energy"] = round(val / 1000, 2)  # Convert Wh to kWh
            
            _LOGGER.debug("Parsed values: %s", result)
            return result
            
        except Exception as err:
            _LOGGER.error("Error parsing inverter values: %s", err)
            return result

    async def test_connection(self) -> bool:
        """Test if we can connect to the inverter."""
        try:
            if await self.login():
                await self.logout()
                return True
            return False
        except Exception as err:
            _LOGGER.error("Connection test failed: %s", err)
            return False

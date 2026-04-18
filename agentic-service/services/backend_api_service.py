"""
Agentic Service — Backend API Service
=======================================
HTTP client for calling the existing Express backend (:5000).
All tools and agents use this service to interact with existing APIs.
"""

import httpx
from config import settings
from utils.logger import setup_logger

log = setup_logger("backend_api")


class BackendAPIService:
    """Async HTTP client for the Express backend."""

    def __init__(self):
        self.base_url = settings.BACKEND_BASE_URL.rstrip("/")
        self.timeout = settings.BACKEND_TIMEOUT

    async def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make an HTTP request to the backend."""
        url = f"{self.base_url}{path}"
        log.info(f"{method.upper()} {url}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                data = response.json()
                return data
        except httpx.TimeoutException:
            log.error(f"Timeout calling {url}")
            raise
        except httpx.HTTPStatusError as e:
            log.error(f"HTTP {e.response.status_code} from {url}")
            raise
        except Exception as e:
            log.error(f"Request failed: {url} — {e}")
            raise

    async def get(self, path: str, params: dict = None) -> dict:
        """GET request to backend."""
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: dict = None) -> dict:
        """POST request to backend."""
        return await self._request("POST", path, json=json)

    # ── Convenience methods for existing APIs ────────────────────────

    async def get_farmer(self, farmer_id: str) -> dict:
        """Fetch farmer profile."""
        return await self.get(f"/api/farmers/{farmer_id}")

    async def get_farms(self, farmer_id: str) -> dict:
        """Fetch farms for a farmer."""
        return await self.get("/api/farms", params={"farmer_id": farmer_id})

    async def get_weather(self, district: str, state: str) -> dict:
        """Fetch current weather."""
        return await self.get("/api/weather/current", params={"district": district, "state": state})

    async def get_reminders(self, farmer_id: str) -> dict:
        """Fetch active reminders."""
        return await self.get("/api/reminders", params={"farmer_id": farmer_id})

    async def get_schemes(self, state: str = None) -> dict:
        """Fetch government schemes."""
        params = {"state": state} if state else {}
        return await self.get("/api/schemes", params=params)

    async def get_market_prices(self, commodity: str, state: str) -> dict:
        """Fetch market prices."""
        return await self.get("/api/market/prices", params={"commodity": commodity, "state": state})

    async def health_check(self) -> bool:
        """Check if the Express backend is reachable."""
        try:
            result = await self.get("/api/health")
            return result.get("status") == "ok"
        except Exception:
            return False


# Singleton instance
backend_api = BackendAPIService()

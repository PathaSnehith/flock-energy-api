
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_URL = "https://urja-ops.flockenergy.tech"


class PortalClient:
    def _get_headers(self):
        cookie = os.getenv("PORTAL_COOKIE", "").strip()

        if not cookie:
            raise RuntimeError(
                "PORTAL_COOKIE is missing from the .env file"
            )

        return {
            "Accept": "application/json, */*",
            "Referer": f"{BASE_URL}/meters",
            "Cookie": cookie,
        }

    async def _get_json(self, url, params=None):
        headers = self._get_headers()

        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                url,
                params=params,
                headers=headers,
            )

            if response.status_code in (401, 403):
                raise RuntimeError(
                    f"Portal authentication failed: HTTP "
                    f"{response.status_code}. Update your .env "
                    "with a valid session cookie."
                )

            response.raise_for_status()

            try:
                return response.json()
            except ValueError as exc:
                raise RuntimeError(
                    "Portal returned a non-JSON response"
                ) from exc

    async def search_meters(self, query="", page=1):
        return await self._get_json(
            f"{BASE_URL}/portal/meters/search",
            params={"q": query, "page": page},
        )

    async def get_meter_energy(self, meter_id: str):
        return await self._get_json(
            f"{BASE_URL}/portal/meters/{meter_id}/energy"
        )

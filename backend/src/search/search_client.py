from typing import Any, Literal

from curl_cffi import AsyncSession
from curl_cffi.requests import Response
from fastapi import HTTPException


class Session:
    def __init__(self):
        self.session: AsyncSession | None = None

    async def get_session(self) -> AsyncSession:
        if self.session is None or self.session._closed:
            self.session = AsyncSession(impersonate="chrome", timeout=10)
        return self.session

    async def _request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        *,
        params: dict | None = None,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> Response:
        session = await self.get_session()
        try:
            return await session.request(
                method, url, params=params, headers=headers, json=json
            )
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail="External search provider is currently unavailable or returned an error.",
            ) from e

    async def post_json(
        self,
        url: str,
        *,
        params: dict | None = None,
        headers: dict | None = None,
        payload: dict | None = None,
    ) -> dict[str, Any]:
        response = await self._request(
            "POST", url, params=params, headers=headers, json=payload
        )

        return response.json()

    async def fetch_html(self, url: str) -> str:
        response = await self._request("GET", url)
        return response.text

    async def close_conn(self):
        if self.session and not self.session._closed:
            await self.session.close()


session = Session()

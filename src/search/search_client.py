from typing import Any

from curl_cffi import AsyncSession
from fastapi import HTTPException


class Session:
    def __init__(self):
        self.session: AsyncSession | None = None

    async def get_session(self) -> AsyncSession:
        if self.session is None or self.session._closed:
            self.session = AsyncSession(impersonate="chrome", timeout=10)
        return self.session

    async def search(
        self,
        url: str,
        params: dict | None = None,
        heasders: dict | None = None,
        payload: dict | None = None,
    ) -> dict[str, Any]:
        session = await self.get_session()
        try:
            if payload or params:
                resp = await session.post(
                    url=url, params=params, headers=heasders, json=payload
                )
                return resp.json()

            resp = await session.get(url=url)
            return resp.text
        except Exception as e: # noqa: BLE001
            print(e)
            raise HTTPException(
                status_code=502,
                detail="External search provider is currently unavailable or returned an error.",
            )

    async def close_conn(self):
        if self.session and not self.session._closed:
            await self.session.close()


session = Session()

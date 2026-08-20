from curl_cffi import AsyncSession


class Session:
    def __init__(self):
        self.session: AsyncSession | None = None

    async def get_session(self) -> AsyncSession:
        if self.session is None or self.session._closed:
            self.session = AsyncSession(impersonate="chrome")
        return self.session

    async def search(self, url: str, params: dict | None = None) -> dict:
        session = await self.get_session()
        try:
            if params:
                resp = await session.get(url=url, params=params)
                return resp.json()
            resp = await session.get(url=url)
            return resp.text
        except Exception as e:
            print(e)

    async def close_conn(self):
        if self.session and not self.session.closed:
            await self.session.close()


session = Session()

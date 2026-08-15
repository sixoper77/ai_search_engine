from asyncio import gather

from config import settings
from src.search.base import BaseSearch

from .search_client import session


class SearxngSearch(BaseSearch):
    searxng_url = settings.searxng_url

    @classmethod
    async def search(cls, query) -> dict:
        params = {"q": query, "format": "json",}  # q: "categories": "images" # format
        result = await session.search(cls.searxng_url, params=params)
        return result

    async def search_photo(query: str,): ...

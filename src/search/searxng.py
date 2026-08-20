import asyncio

from config import settings
from src.search.base import BaseSearch

from .search_client import session


class SearxngSearch(BaseSearch):
    searxng_url = settings.searxng_url

    @classmethod
    async def search(cls, query: str, photo_query: str, language: str) -> dict:
        async with asyncio.TaskGroup() as tg:
            task_url = tg.create_task(cls.search_urls(query, language))
            task_photo = tg.create_task(cls.search_photo(photo_query, language))
        return task_url.result(),task_photo.result() 

    @classmethod
    async def search_urls(cls, query: str, language: str) -> dict:
        params = {
            "q": query,
            "language": language,
            "categories": "general",
            "format": "json",
        }  # q: "categories": "images" # format
        result = await session.search(cls.searxng_url, params=params)
        return result

    @classmethod
    async def search_photo(cls, query: str, language: str) -> dict:
        result = await session.search(
            cls.searxng_url,
            params={
                "q": query,
                "language": language,
                "format": "json",
                "categories": "images",
            },
        )
        return result

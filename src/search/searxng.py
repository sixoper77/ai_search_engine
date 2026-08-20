import asyncio

from config import settings
from src.search.base import BaseSearch

from .search_client import session


class SearxngSearch(BaseSearch):
    searxng_url = settings.searxng_url

    @classmethod
    async def search(cls, query: str, photo_query: str, language: str):
        tasks_photo = []
        tasks_url = []
        async with asyncio.TaskGroup() as tg:
            task = tg.create_task(cls.search_urls(query, language))
            tasks_url.append(task)
            task2 = tg.create_task(cls.search_photo(photo_query, language))
            tasks_photo.append(task2)
        photo_urls = [photo.result() for photo in tasks_photo]
        urls = [url.result() for url in tasks_url]
        return urls, photo_urls

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

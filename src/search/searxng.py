import asyncio

from config import settings
from src.search.base import BaseSearch

from .search_client import session


class SearxngSearch(BaseSearch):
    searxng_url = settings.searxng_url

    @classmethod
    async def search(cls, queries: list[str], photo_query: str, language: str) -> dict:
        async with asyncio.TaskGroup() as tg:
            url_tasks = [tg.create_task(cls.search_urls(q, language)) for q in queries]
            task_photo = tg.create_task(cls.search_photos(photo_query, language))
        url_results = [task.result() for task in url_tasks]
        return url_results, task_photo.result()

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
    async def search_photos(cls, query: str, language: str) -> dict:
        params = {
            "q": query,
            "language": language,
            "format": "json",
            "categories": "images",
        }
        result = await session.search(cls.searxng_url, params=params)
        return result

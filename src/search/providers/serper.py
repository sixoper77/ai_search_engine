from asyncio import TaskGroup
from typing import ClassVar

from config import settings
from src.search.base import BaseSearch
from src.search.search_client import session


class SerperCLient(BaseSearch):
    url = settings.serper_url
    headers: ClassVar[dict] = {
        "X-API-KEY": settings.serper_api_key,
        "Content-Type": "application/json",
    }

    @classmethod
    async def search(
        cls,
        queries: list[str],
        photo_query: str,
        type: str,
        country: str,
        language: str,
    ):
        async with TaskGroup() as tg:
            url_tasks = [
                tg.create_task(cls.search_urls(q, type, country, language))
                for q in queries
            ]
            task_photo = tg.create_task(
                cls.search_photos(photo_query, country, language)
            )
        url_results = [task.result() for task in url_tasks]
        return url_results, task_photo.result()

    @classmethod
    async def search_urls(cls, q: str, type: str, county: str, language: str):
        url = f"{cls.url}/{type}"

        payload = {
            "q": q,
            "gl": county,
            "hl": language,
        }
        response = await session.search(url, payload=payload, heasders=cls.headers)
        return response

    @classmethod
    async def search_photos(cls, q: str, county: str, language: str):
        url = f"{cls.url}/images"
        payload = {
            "q": q,
            "gl": county,
            "hl": language,
        }
        response = await session.search(url, payload=payload, heasders=cls.headers)
        return response


serper_client = SerperCLient()

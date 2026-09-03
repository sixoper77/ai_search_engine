from asyncio import TaskGroup
from typing import ClassVar

from config import settings
from src.llm.schemas import SerperGeneralResponse, SerperPhotosResult
from src.search.base import BaseSearch
from src.search.schemas import SerperSearchSchema
from src.search.search_client import session


class SerperCLient(
    BaseSearch[
        SerperSearchSchema, tuple[list[SerperGeneralResponse], SerperPhotosResult]
    ]
):
    url = settings.serper_url
    headers: ClassVar[dict] = {
        "X-API-KEY": settings.serper_api_key,
        "Content-Type": "application/json",
    }

    # queries: list[str],photo_query: str,type: str,country: str,language: str,
    async def search(
        self, data: SerperSearchSchema
    ) -> tuple[list[SerperGeneralResponse], SerperPhotosResult]:
        queries, photo_query, type, country, language = (
            data.queries,
            data.photo_query,
            data.type,
            data.country,
            data.language,
        )
        async with TaskGroup() as tg:
            url_tasks = [
                tg.create_task(self.search_urls(q, type, country, language))
                for q in queries
            ]
            task_photo = tg.create_task(
                self.search_photos(photo_query, country, language)
            )
        url_results = [task.result() for task in url_tasks]
        return url_results, task_photo.result()

    async def search_urls(
        self, q: str, type: str, county: str, language: str
    ) -> SerperGeneralResponse:
        url = f"{self.url}/{type}"

        payload = {
            "q": q,
            "gl": county,
            "hl": language,
        }
        response = await session.search(url, payload=payload, heasders=self.headers)
        return SerperGeneralResponse(**response)

    async def search_photos(
        self, q: str, county: str, language: str
    ) -> SerperPhotosResult:
        url = f"{self.url}/images"
        payload = {
            "q": q,
            "gl": county,
            "hl": language,
        }
        response = await session.search(url, payload=payload, heasders=self.headers)
        return SerperPhotosResult(**response)


serper_client = SerperCLient()

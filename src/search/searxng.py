import asyncio

from config import settings
from src.llm.schemas import SearxngGeneralResponse, SearxngImageResponse
from src.search.base import BaseSearch

from .schemas import SearxngSearchSchema
from .search_client import session


class SearxngSearch(
    BaseSearch[
        SearxngSearchSchema, tuple[list[SearxngGeneralResponse], SearxngImageResponse]
    ]
):
    def __init__(self) -> None:
        if not settings.searxng_url:
            raise ValueError("SEARXNG_URL is not configured")
        self.searxng_url: str = settings.searxng_url

    async def search(
        self, data: SearxngSearchSchema
    ) -> tuple[list[SearxngGeneralResponse], SearxngImageResponse]:
        language, queries, photo_query = (
            data.language,
            data.search_links,
            data.search_photos,
        )
        async with asyncio.TaskGroup() as tg:
            url_tasks = [tg.create_task(self.search_urls(q, language)) for q in queries]
            task_photo = tg.create_task(self.search_photos(photo_query, language))
        url_results = [task.result() for task in url_tasks]
        return url_results, task_photo.result()

    async def search_urls(self, query: str, language: str) -> SearxngGeneralResponse:
        params = {
            "q": query,
            "language": language,
            "categories": "general",
            "format": "json",
        }  # q: "categories": "images" # format
        result = await session.search(self.searxng_url, params=params)
        print(result)
        return SearxngGeneralResponse.model_validate(result)

    async def search_photos(self, query: str, language: str) -> SearxngImageResponse:
        params = {
            "q": query,
            "language": language,
            "format": "json",
            "categories": "images",
        }
        result = await session.search(self.searxng_url, params=params)
        print(result)
        return SearxngImageResponse.model_validate(result)


searxng_client = SearxngSearch()

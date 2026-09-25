import asyncio
from collections.abc import Iterator, Sequence

from trafilatura import extract

from src.llm.schemas import (
    ParseData,
    ResponseSchema,
    TavilyResponse,
)


class Parser:
    @classmethod
    async def parse(
        cls,
        links_response: Sequence[ResponseSchema],
        photos_response: ResponseSchema,
    ) -> ParseData:
        async with asyncio.TaskGroup() as tg:
            links = tg.create_task(asyncio.to_thread(cls.parse_links, links_response))
            photos = tg.create_task(
                asyncio.to_thread(cls.parse_photos, photos_response)
            )
        return ParseData(links=links.result(), photos=photos.result())

    @staticmethod
    def parse_photos(response: ResponseSchema, photo_results: int = 4) -> list[str]:
        urls = (url.img_src for url in response.results)
        return list(dict.fromkeys(urls))[:photo_results]

    @staticmethod
    def parse_links(
        responses: Sequence[ResponseSchema], url_results: int = 7
    ) -> list[str]:
        all_urls = (res.url for response in responses for res in response.results)
        return list(dict.fromkeys(all_urls))[:url_results]

    @staticmethod
    def parse_tavily(response: list[TavilyResponse]) -> Iterator[tuple[str, str]]:
        return ((res.url, res.content) for res in response)

    @staticmethod
    async def parse_html(html: str) -> str | None:
        result = await asyncio.to_thread(extract, html, output_format="markdown")
        return result

import asyncio

from trafilatura import extract

from src.llm.schemas import ParseData, SearxngGeneralResponse, SearxngImageResponse


class Parser:
    @classmethod
    async def parse(
        cls,
        links_response: list[SearxngGeneralResponse],
        photos_response: SearxngImageResponse,
    ) -> ParseData:
        async with asyncio.TaskGroup() as tg:
            links = tg.create_task(asyncio.to_thread(cls.parse_links, links_response))
            photos = tg.create_task(
                asyncio.to_thread(cls.parse_photos, photos_response)
            )
        return ParseData(links=links.result(), photos=photos.result())

    @staticmethod
    def parse_photos(
        response: SearxngImageResponse, photo_results: int = 4
    ) -> list[str]:
        urls = (url.img_src for url in response.results)
        return list(dict.fromkeys(urls))[:photo_results]

    @staticmethod
    def parse_links(
        responses: list[SearxngGeneralResponse], url_results: int = 7
    ) -> list[str]:
        all_urls = (res.url for response in responses for res in response.results)
        return list(dict.fromkeys(all_urls))[:url_results]

    @staticmethod
    async def parse_html(html: str) -> str | None:
        result = await asyncio.to_thread(extract, html, output_format="markdown")
        return result

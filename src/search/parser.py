import asyncio

from trafilatura import extract


class Parser:
    @classmethod
    async def parse(cls, links_response: dict[str], photos_response: dict[str]):
        async with asyncio.TaskGroup() as tg:
            links = tg.create_task(
                asyncio.to_thread(cls.parse_links, links_response))
            photos = tg.create_task(
                asyncio.to_thread(cls.parse_photos, photos_response)
            )
        return links.result(), photos.result()

    @staticmethod
    def parse_photos(response: list[dict], photo_results: int = 4) -> list:
        if response is None:
            return []
        results = response["results"]
        return list(dict.fromkeys(url["img_src"] for url in results))[:photo_results]

    @staticmethod
    def parse_links(response: list[dict], url_results: int = 7):
        if response is None:
            return []
        results = response[0]["results"]
        return list(dict.fromkeys(url["url"] for url in results))[:url_results]

    @staticmethod
    async def parse_html(html) -> str:
        result = await asyncio.to_thread(extract, html, output_format="markdown")
        return result

import asyncio

from trafilatura import extract


class Parser:
    @staticmethod
    def parse_photos(response: dict, photo_results: int = 4) -> list:
        print(response)
        results = response[0]["results"]
        return list(dict.fromkeys(url["img_src"] for url in results))[:photo_results]

    @staticmethod
    def parse_links(response: list[dict], url_results: int = 7):
        print(response)
        results = response[0]["results"]
        return list(dict.fromkeys(url["url"] for url in results))[:url_results]

    @staticmethod
    async def parse_html(html) -> str:
        result = await asyncio.to_thread(extract, html, output_format="markdown")
        return result

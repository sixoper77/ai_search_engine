import asyncio

from trafilatura import extract

from .search_client import session


def parse_urls(
    response: dict,
    photos: bool | None = False,
    photo_results: int = 4,
    url_results: int = 7,
) -> list[str]:
    res_from_resp = response["results"]
    if not photos:
        return [url["url"] for url in res_from_resp][:url_results]
    return [url["img_src"] for url in response][:photo_results]


async def parse_html(html) -> str:
    result = await asyncio.to_thread(extract,html, output_format="markdown")
    return result


async def get_text(htmls:list):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for html in htmls:
            taskk = tg.create_task(parse_html(html))
            tasks.append(taskk)
    results = [task.result() for task in tasks]
    return results

async def search_html(urls: list):
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            taskk = tg.create_task(session.search(url))
            tasks.append(taskk)
    results = [task.result() for task in tasks]
    return results

import asyncio

from .parser import Parser
from .search_client import session


async def get_text(htmls: list) -> list:
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for html in htmls:
            taskk = tg.create_task(Parser.parse_html(html))
            tasks.append(taskk)
    results = [
        " ".join(task.result().split(" "))[:3200]
        for task in tasks
        if task is not None and task.result() is not None
    ]

    return list(dict.fromkeys(results))


async def search_html(urls: list) -> list:
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            taskk = tg.create_task(session.search(url))
            tasks.append(taskk)
    results = [task.result() for task in tasks]
    return list(dict.fromkeys(results))

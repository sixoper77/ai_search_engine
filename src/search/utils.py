import asyncio

from .parser import Parser
from .search_client import session


async def get_text(htmls: list) -> list:
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for html in htmls:
            taskk = tg.create_task(Parser.parse_html(html))
            tasks.append(taskk)
    all_chunks = []
    for task in tasks:
        text = task.result()
        if text:
            chunk_text = batch_text(text)
            all_chunks.extend(chunk_text)

    return list(dict.fromkeys(all_chunks))


async def search_html(urls: list) -> list:
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            taskk = tg.create_task(session.search(url))
            tasks.append(taskk)
    results = [task.result() for task in tasks]
    return list(dict.fromkeys(results))


def batch_text(text: str, batch_size: int = 1200, overlap: int = 200):
    text = " ".join(text.split())
    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + batch_size, text_len)
        if end < text_len:
            boundary = text.rfind(" ", start, end)
            if boundary != -1 and boundary > start + (batch_size // 2):
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == text_len:
            break
        next_start_raw = end - overlap
        next_start_boundary = text.find(" ", next_start_raw, end)
        if next_start_boundary != -1:
            start = next_start_boundary + 1
        else:
            start = next_start_raw
    return chunks

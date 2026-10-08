import asyncio
from collections.abc import Iterator, Sequence

from src.llm.schemas import (
    QueriesSchema,
    ResponseSchema,
    SerperSchema,
    TavilyResponse,
    TavilySchema,
)
from src.search.parser import Parser

from .schemas import (
    BaseEvent,
    SearchSchema,
    SearxngSearchSchema,
    SerperSearchSchema,
    Source,
    TavilySearchSchema,
)
from .search_client import session


async def get_text(htmls: list[tuple[str, str, str]]) -> list[Source]:
    async def process(hmtl: str, url: str, title: str):
        text = await Parser.parse_html(hmtl)
        if not text:
            return []
        return [Source(text=c, url=url, title=title) for c in batch_text(text)]

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(process(html, url, title)) for html, url, title in htmls
        ]
    all_chunks: list[Source] = []
    for task in tasks:
        all_chunks.extend(task.result())
    seen = {}
    for c in all_chunks:
        seen.setdefault(c.text, c)
    return list(seen.values())


async def search_html(urls: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    async def process(url: str, title: str) -> tuple[str, str, str] | None:
        try:
            html = await session.fetch_html(url)
        except Exception as e:
            print(f"skip {url}: {e}")
            return None
        return html, url, title

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process(url, title)) for url, title in urls]
    return [r for t in tasks if (r := t.result()) is not None]


def batch_text(text: str, batch_size: int = 2000, overlap: int = 300) -> list[str]:
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


async def batch_text_from_list(texts: Iterator[tuple[str, str, str]]) -> list[Source]:
    def process(text: str, url: str, title: str):
        return [Source(text=chunk, url=url, title=title) for chunk in batch_text(text)]

    bat_text = []

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(asyncio.to_thread(process, text, url, title))
            for url, text, title in texts
            if text
        ]

    for task in tasks:
        bat_text.extend(task.result())
    return bat_text


def emit(event: BaseEvent) -> str:
    return f"data: {event.model_dump_json()}\n\n"


def build_searxng_schema(q: str, schema: QueriesSchema) -> SearchSchema:
    return SearxngSearchSchema(
        search_links=schema.search_links,
        search_photos=schema.search_photos,
        language=schema.language,
    )


def build_serper_schema(q: str, schema: SerperSchema) -> SearchSchema:
    return SerperSearchSchema(
        queries=schema.search_links,
        photo_query=schema.search_photos,
        type=schema.search_type,
        country=schema.country,
        language=schema.lang,
    )


def build_tavily_schema(q: str, schema: TavilySchema) -> SearchSchema:
    return TavilySearchSchema(query=q, topic=schema.topic, max_results=7)


async def process_links(
    links_results: Sequence[ResponseSchema], photos_results: ResponseSchema
) -> list[Source]:
    result = await Parser.parse(links_results, photos_results)
    print(result.links)
    sites = await search_html(result.links)
    return await get_text(sites)


async def process_tavily(
    data: Sequence[ResponseSchema], photos_results: ResponseSchema
) -> list[Source]:
    async def process(
        url: str,
        content: str,
        title: str,
    ):
        return [Source(text=text, url=url, title=title) for text in batch_text(content)]

    parsed_data: list[TavilyResponse] = [item for page in data for item in page.results]
    results = Parser.parse_tavily(parsed_data)
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(process(url, content, title))
            for url, content, title in results
        ]
    all_chunks: list[Source] = []
    for task in tasks:
        all_chunks.extend(task.result())
    seen = {}
    for c in all_chunks:
        seen.setdefault(c.text, c)
    return list(seen.values())

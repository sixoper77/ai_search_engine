# This code is dirty and it isn't final yet
import asyncio

from fastapi import FastAPI

from src.llm.base import llm
from src.llm.schemas import QueriesSchema, TavilySchema
from src.matcher.match import match_results
from src.search.parser import Parser
from src.search.providers.tavily import tavily_client
from src.search.searxng import SearxngSearch
from src.search.utils import batch_text, get_text, search_html

app = FastAPI()


@app.get("/search/searxng")
async def send_request(q: str):
    query = await llm.get_query(q, QueriesSchema)
    q_links, photo_links, language = (
        query.search_links,
        query.search_photos,
        query.language,
    )
    print(q_links)
    print(photo_links)

    links_results, photos_results = await SearxngSearch.search(
        q_links, photo_links, language
    )
    result, photos = await Parser.parse(links_results, photos_results)

    sites = await search_html(result)
    text = await get_text(sites)
    print(text)
    match_result = await asyncio.to_thread(match_results, q, text)
    stream_response = await llm.astream(q, match_result)
    print(stream_response)
    print(q_links)


@app.get("/search/tavily")
async def tavily_search(q: str):
    query = await llm.get_query(q, TavilySchema)
    tavily_query = query.topic
    print(tavily_query)
    texts, images = await tavily_client.search(q, tavily_query)
    print(texts)
    print(f"Получено текстов от поиска: {len(texts)}")
    bat_text = []
    tasks = []

    async with asyncio.TaskGroup() as tg:
        for t in texts:
            if t:
                task = tg.create_task(asyncio.to_thread(batch_text, t))
                tasks.append(task)

    for task in tasks:
        bat_text.extend(task.result())
    print(f"Сгенерировано чанков: {len(bat_text)}")
    match_result = await asyncio.to_thread(match_results, q, bat_text)
    stream_response = await llm.astream(q, match_result)
    print(stream_response)

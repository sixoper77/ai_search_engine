# This code is dirty and it isn't final yet
import asyncio

from fastapi import FastAPI

from src.llm.base import llm
from src.llm.schemas import (
    QueriesSchema,
    SerperPhotosList,
    SerperResponseList,
    SerperSchema,
    TavilySchema,
)
from src.matcher.match import match_results
from src.search.parser import Parser
from src.search.providers.serper import serper_client
from src.search.providers.tavily import tavily_client
from src.search.searxng import SearxngSearch
from src.search.utils import batch_text_from_list, get_text, search_html

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
    bat_text = await batch_text_from_list(texts)
    print(f"Сгенерировано чанков: {len(bat_text)}")
    match_result = await asyncio.to_thread(match_results, q, bat_text)
    stream_response = await llm.astream(q, match_result)
    print(stream_response)


@app.get("/search/serper/")
async def serper_search(q: str):
    query = await llm.get_query(q, SerperSchema)
    texts, photos = await serper_client.search(
        query.search_links,
        query.search_photos,
        query.search_type,
        query.country,
        query.lang,
    )
    all_text_results = [SerperResponseList(**res) for res in texts]
    all_photos_results = SerperPhotosList(**photos)
    links = [
        res.link for text_results in all_text_results for res in text_results.organic
    ]
    sites = await search_html(links)
    text = await get_text(sites)
    match_result = await asyncio.to_thread(match_results, q, text)
    stream_response = await llm.astream(q, match_result)
    print(stream_response)
    print(query.search_links)
    

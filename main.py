# This code is dirty and it isn't final yet
import asyncio

from fastapi import FastAPI, HTTPException, status

from src.llm.base import llm
from src.llm.schemas import (
    QueriesSchema,
    SerperSchema,
    TavilySchema,
)
from src.matcher.match import match_results
from src.search.parser import Parser
from src.search.providers.searxng import searxng_client
from src.search.providers.serper import serper_client
from src.search.providers.tavily import tavily_client
from src.search.registry import providers
from src.search.schemas import (
    SearxngSearchSchema,
    SerperSearchSchema,
    TavilySearchSchema,
)
from src.search.utils import batch_text_from_list, get_text, search_html

app = FastAPI()


@app.get("/search/searxng")
async def send_request(q: str):
    query = await llm.get_query(q, QueriesSchema)
    schema = SearxngSearchSchema(
        search_links=query.search_links,
        search_photos=query.search_photos,
        language=query.language,
    )
    links_results, photos_results = await searxng_client.search(schema)
    print(links_results)
    print(photos_results)
    result = await Parser.parse(links_results, photos_results)

    sites = await search_html(result.links)
    text = await get_text(sites)
    match_result = await asyncio.to_thread(match_results, q, text)
    async for token in llm.astream(q, match_result):
        print(token, end="", flush=True)


@app.get("/search/serper/")
async def serper_search(q: str):
    query = await llm.get_query(q, SerperSchema)
    print(query.search_type)
    schema = SerperSearchSchema(
        queries=query.search_links,
        photo_query=query.search_photos,
        type=query.search_type,
        country=query.country,
        language=query.lang,
    )
    links_results, photos_results = await serper_client.search(schema)
    result = await Parser.parse(links_results, photos_results)
    print(result.links)
    sites = await search_html(result.links)
    text = await get_text(sites)
    match_result = await asyncio.to_thread(match_results, q, text)
    async for token in llm.astream(q, match_result):
        print(token, end="", flush=True)
    print(query.search_links)


@app.get("/search/tavily")
async def tavily_search(q: str):
    query = await llm.get_query(q, TavilySchema)
    schema = TavilySearchSchema(query=q, topic=query.topic, max_results=7)
    responses = await tavily_client.search(schema)
    texts = Parser.parse_tavily(responses.results)
    bat_text = await batch_text_from_list(texts)
    match_result = await asyncio.to_thread(match_results, q, bat_text)
    async for token in llm.astream(q, match_result):
        print(token, end="", flush=True)


@app.get("search/pro/search/")
async def pro_search(q: str, provider_name: str):
    provider = providers.get(provider_name)
    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The query was entered incorrectly, or such a provider does not exist.",
        )
    if q is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The query is empty"
        )

    # query = await llm.get_query(q, provider.schema)
    # schema = provider.builder(q, query)
    # texts, photos = await provider.client.search(schema)
    # process = await provider.process(texts, photos)

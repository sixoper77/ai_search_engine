import asyncio

from fastapi import FastAPI

from src.llm.base import llm
from src.matcher.match import match_results
from src.search.parser import Parser
from src.search.searxng import SearxngSearch
from src.search.utils import get_text, search_html

app = FastAPI()


@app.get("/search/searxng")
async def send_request(q: str):
    query = await llm.get_query(q)
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

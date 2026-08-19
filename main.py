import asyncio

from fastapi import FastAPI

from src.llm.base import llm
from src.search.searxng import SearxngSearch
from src.search.utils import get_text, parse_urls, search_html

app = FastAPI()


@app.get("/search/searxng")
async def send_request(q: str):
    query = await llm.get_query(q)
    q_links = query.search_links
    print(q_links)
    resp = await SearxngSearch.search(q_links)
    result = await asyncio.to_thread(parse_urls, resp)
    print(result)
    sites = await search_html(result)
    text = await get_text(sites)
    print(text)

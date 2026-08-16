import asyncio

from fastapi import FastAPI

from src.search.searxng import SearxngSearch
from src.search.utils import get_text, parse_urls, search_html

app = FastAPI()


@app.get("/search/searxng")
async def send_request(q: str):
    resp = await SearxngSearch.search(q)
    result = await asyncio.to_thread(parse_urls, resp)
    sites = await search_html(result)
    text = await get_text(sites)
    print(text)
    # print(result)

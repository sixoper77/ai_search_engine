import asyncio

from fastapi import FastAPI

from src.search.searxng import SearxngSearch
from src.search.utils import parse_urls

app = FastAPI()


@app.get("/search/searxng")
async def send_request(q: str):
    resp = await SearxngSearch.search(q)
    result = await asyncio.to_thread(parse_urls, resp)
    print(result)

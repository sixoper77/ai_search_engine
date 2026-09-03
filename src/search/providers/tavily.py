from tavily import AsyncTavilyClient

from config import settings
from src.llm.schemas import TavilyGeneralResponse
from src.search.base import BaseSearch
from src.search.schemas import SearchSchema

TAVILY_API_KEY = settings.tavily_api_key
if TAVILY_API_KEY is None:
    raise ValueError("TAVILY API KEY not found")


class TavilySearch(BaseSearch[SearchSchema, TavilyGeneralResponse]):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client: AsyncTavilyClient | None = None

    def get_session(self):
        if self.client is None:
            self.client = AsyncTavilyClient(api_key=self.api_key)
        return self.client

    def close_session(self):
        session = self.get_session()
        if session:
            session.close()

    # query: str, topic: str, max_results: int = 7
    async def search(self, data: SearchSchema) -> TavilyGeneralResponse:
        query, max_results, topic = data.query, data.max_results, data.topic
        tavily_client = self.get_session()
        response = await tavily_client.search(
            query,
            include_images=True,
            max_results=max_results,
            search_depth="advanced",
            topic=topic,
        )
        return TavilyGeneralResponse(**response)


tavily_client = TavilySearch(TAVILY_API_KEY)

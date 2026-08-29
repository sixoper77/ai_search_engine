from tavily import AsyncTavilyClient

from config import settings
from src.search.base import BaseSearch

TAVILY_API_KEY = settings.tavily_api_key


class TavilySearch(BaseSearch):
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

    async def search(self, query: str, topic: str, max_results: int = 7):
        tavily_client = self.get_session()
        response = await tavily_client.search(
            query,
            include_images=True,
            max_results=max_results,
            search_depth="advanced",
            topic=topic,
        )
        all_images = response["images"][:4]
        results = response["results"]
        all_content = [result["content"] for result in results]
        return all_content, all_images


tavily_client = TavilySearch(TAVILY_API_KEY)

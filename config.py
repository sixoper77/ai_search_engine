import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    serper_api_key = os.getenv("SERPER_API_KEY")
    bing_api_key = os.getenv("BING_API_KEY")
    searxng_url = os.getenv("SEARXNG_URL")
    time_range = os.getenv("TIME_RANGE", "year")  # day month year


settings = Settings()

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    bing_api_key = os.getenv("BING_API_KEY")
    searxng_url = os.getenv("SEARXNG_URL")

    serper_api_key = os.getenv("SERPER_API_KEY")
    serper_url = os.getenv("SERPER_URL")
    
    time_range = os.getenv("TIME_RANGE", "year")  # day month year

    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL")

    gemeni_api_key = os.getenv("GEMINI_API_KEY")
    gemeni_model = os.getenv("GEMENI_MODEL")

    llama_model = os.getenv("LLAMA_MODEL")
    llama_url = os.getenv("LLAMA_URL")

    @classmethod
    def get_provider(cls):
        providers = {
            "tavily": cls.tavily_api_key,
            "serper": cls.serper_api_key,
            "bing": cls.bing_api_key,
            "searxng": cls.searxng_url,
        }
        for name, value in providers.items():
            if value:
                return name, value

        return None, None

    @classmethod
    def get_model_and_key(cls):
        if cls.openai_api_key and cls.openai_model:
            return (None,cls.openai_model)
        if cls.gemeni_api_key and cls.gemeni_model:
            return  (None,cls.gemeni_model)
        if cls.llama_model and cls.llama_url:
            return (cls.llama_url, cls.llama_model)
        return (None, None)


settings = Settings()

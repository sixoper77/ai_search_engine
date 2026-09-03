from __future__ import annotations

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    tavily_api_key: str | None = None
    bing_api_key: str | None = None
    searxng_url: str | None = None
    serper_api_key: str | None = None
    serper_url: str | None = None

    time_range: Literal["day", "month", "year"] = "year"

    openai_api_key: str | None = None
    openai_model: str | None = None

    gemini_api_key: str | None = None
    gemini_model: str | None = None

    llama_model: str | None = None
    llama_url: str | None = None

    def get_model_and_key(self) -> tuple[str | None, str]:
        if self.openai_api_key and self.openai_model:
            return (None, self.openai_model)
        if self.gemini_api_key and self.gemini_model:
            return (None, self.gemini_model)
        if self.llama_model and self.llama_url:
            return (self.llama_url, self.llama_model)
        raise ValueError(
            "Add model,api key or model url(if your model is local) to .env file"
        )

    def get_provider(self) -> tuple[str, str] | None:
        providers = {
            "tavily": self.tavily_api_key,
            "serper": self.serper_api_key,
            "bing": self.bing_api_key,
            "searxng": self.searxng_url,
        }
        for name, value in providers.items():
            if value:
                return name, value
        return None


settings = Settings()

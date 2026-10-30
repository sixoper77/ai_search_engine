from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent
ENV_PATH = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH) if ENV_PATH.exists() else ".env",
        extra="ignore",
    )
    database_url: str = f"sqlite+aiosqlite:///{BACKEND_DIR / 'app.db'}"

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

    groq_api_key: str | None = None
    qwen_model: str | None = None

    @property
    def resolved_database_url(self) -> str:
        if self.database_url.startswith("sqlite+aiosqlite:///./"):
            rel_path = self.database_url.replace("sqlite+aiosqlite:///./", "")
            return f"sqlite+aiosqlite:///{BACKEND_DIR / rel_path}"
        return self.database_url

    def get_model_and_key(self) -> tuple[str | None, str]:
        if self.openai_api_key and self.openai_model:
            return (None, self.openai_model)
        if self.gemini_api_key and self.gemini_model:
            return (None, self.gemini_model)
        if self.llama_model and self.llama_url:
            return (self.llama_url, self.llama_model)
        if self.groq_api_key and self.qwen_model:
            return (None, self.qwen_model)
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

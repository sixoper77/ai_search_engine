from typing import Annotated, Literal

from pydantic import BaseModel, Field

from .enums import Prompts

SearxngLocales = Literal["ru-RU", "en-US", "uk-UA", "de-DE", "fr-FR"]
TavilyTopics = Literal["general", "news", "finance"]


class AskSchema(BaseModel):
    pass


class QueriesSchema(AskSchema):
    search_links: Annotated[list[str], Field(description=Prompts.PROMPT_URL)]
    search_photos: Annotated[str, Field(description=Prompts.PROMPT_PHOTO)]
    language: Annotated[SearxngLocales, Field(description=Prompts.GET_LANGUAGE_LOCALES)]


class TavilySchema(AskSchema):
    topic: Annotated[TavilyTopics, Field(description=Prompts.TAVILY_TOPICS)]

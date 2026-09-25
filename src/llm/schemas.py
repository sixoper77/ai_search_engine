from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import Prompts

SearxngLocales = Literal["ru-RU", "en-US", "uk-UA", "de-DE", "fr-FR"]
TavilyTopics = Literal["general", "news", "finance"]
SerperTypes = Literal["search", "reviews", "news", "shopping", "scholar", "patents"]


class AskSchema(BaseModel):
    pass


class ResponseSchema(BaseModel):
    results: list[Any]


class QueriesSchema(AskSchema):
    search_links: Annotated[list[str], Field(description=Prompts.PROMPT_URL)]
    search_photos: Annotated[str, Field(description=Prompts.PROMPT_PHOTO)]
    language: Annotated[SearxngLocales, Field(description=Prompts.GET_LANGUAGE_LOCALES)]


class TavilySchema(AskSchema):
    topic: Annotated[TavilyTopics, Field(description=Prompts.TAVILY_TOPICS)]


class SerperSchema(QueriesSchema):
    search_type: Annotated[SerperTypes, Field(description=Prompts.SERPER_TYPES)]

    @property
    def lang(self) -> str:
        return self.language.split("-")[0]

    @property
    def country(self) -> str:
        return self.language.split("-")[1].lower()


class SerperResponse(BaseModel):
    title: str
    url: Annotated[str, Field(alias="link")]
    snippet: str


class SerperGeneralResponse(ResponseSchema):
    results: list[SerperResponse] = Field(default_factory=list, alias="organic")


class SerperPhotos(BaseModel):
    img_src: str = Field(alias="imageUrl")


class SerperPhotosResult(ResponseSchema):
    results: list[SerperPhotos] = Field(default_factory=list, max_length=4)

    @field_validator("results", mode="before")
    @classmethod
    def cut_list(cls, v: Any) -> Any:
        return v[:4] if isinstance(v, list) else v


class ParseData(BaseModel):
    links: Annotated[list[str], Field(default_factory=list)]
    photos: Annotated[list[str], Field(default_factory=list)]


class SearxngResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    url: str


class SearxngGeneralResponse(ResponseSchema):
    model_config = ConfigDict(extra="allow")
    results: Annotated[list[SearxngResult], Field(default_factory=list)]


class SearxngPhotoResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    img_src: str


class SearxngImageResponse(ResponseSchema):
    model_config = ConfigDict(extra="allow")
    results: Annotated[list[SearxngPhotoResult], Field(default_factory=list)]

    @field_validator("results", mode="before")
    @classmethod
    def clean_results(cls, v: Any) -> Any:
        if not isinstance(v, list):
            return v
        seen: set[str] = set()
        out = []
        for r in v:
            src = r.get("img_src") if isinstance(r, dict) else None
            if src and src not in seen and not src.lower().endswith(".heic"):
                seen.add(src)
                out.append(r)
        return out


class TavilyResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    content: str
    url: str


class TavilyGeneralResponse(ResponseSchema):
    model_config = ConfigDict(extra="allow")
    query: str
    images: list[str]
    results: list[TavilyResponse]

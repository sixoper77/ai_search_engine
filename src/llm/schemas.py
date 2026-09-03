from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import Prompts

SearxngLocales = Literal["ru-RU", "en-US", "uk-UA", "de-DE", "fr-FR"]
TavilyTopics = Literal["general", "news", "finance"]
SerperTypes = Literal["search", "reviews", "news", "shopping", "scholar", "patents"]


class AskSchema(BaseModel):
    pass


class ResponseSchema(BaseModel):
    pass


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
    link: str
    snippet: str


class SerperGeneralResponse(ResponseSchema):
    organic: list[SerperResponse] = Field(default_factory=list)


class SerperPhotos(BaseModel):
    image_url: str = Field(alias="imageUrl")


class SerperPhotosResult(ResponseSchema):
    images: list[SerperPhotos] = Field(default_factory=list, max_length=4)

    @field_validator("images", mode="before")
    @classmethod
    def cut_list(cls, v: list) -> list:
        if isinstance(v, list):
            return v[:4]


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


class TavilyResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    content: str


class TavilyGeneralResponse(ResponseSchema):
    model_config = ConfigDict(extra="allow")
    query: str
    images: list[str]
    results: list[TavilyResponse]

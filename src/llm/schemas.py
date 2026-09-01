from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator

from .enums import Prompts

SearxngLocales = Literal["ru-RU", "en-US", "uk-UA", "de-DE", "fr-FR"]
TavilyTopics = Literal["general", "news", "finance"]
SerperTypes = Literal["search", "reviews", "news", "shopping", "scholar", "patents"]


class AskSchema(BaseModel):
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


class SerperResponseList(BaseModel):
    organic: list[SerperResponse] = Field(default_factory=list)


class SerperPhotos(BaseModel):
    image_url: str = Field(alias="imageUrl")


class SerperPhotosList(BaseModel):
    images: list[SerperPhotos] = Field(default_factory=list, max_length=4)

    @field_validator("images", mode="before")
    @classmethod
    def cut_list(cls, v: list) -> list:
        if isinstance(v, list):
            return v[:4]
        

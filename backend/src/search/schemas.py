from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.llm.enums import Prompts
from src.llm.schemas import AskSchema


class BaseEvent(BaseModel):
    pass


class SearchSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    query: str | None = None
    max_results: int | None = None
    topic: str | None = None


class SerperSearchSchema(SearchSchema):
    queries: list[str]
    photo_query: str
    type: str
    country: str
    language: str


class SearxngSearchSchema(SearchSchema):
    search_links: list[str]
    search_photos: str
    language: str


class TavilySearchSchema(SearchSchema):
    pass


class StepSrtartEvent(BaseEvent):
    type: str = "step_start"
    messgae: str
    step: int


class SearchIntentEvent(BaseEvent):
    type: str = "search_intent"
    step: int
    queris: list[str]


class SearchResultsEvent(BaseEvent):
    type: str = "search_results"
    step: int
    sites: list[Source]
    facts_found: int


class InfoEvent(BaseEvent):
    type: str = "info"
    message: str


class ErrorEvent(BaseEvent):
    type: str = "error"
    step: int | None = None
    message: str
    recoverable: bool = True


class DoneEvent(BaseEvent):
    type: str = "done"
    total_steps: int
    total_sources: int
    message: str


class FinalResponseEvent(BaseEvent):
    type: str = "final_answer_chunk"
    text: str


class SitesInfo(BaseModel):
    url: str
    title: str


class SitesInfoEvent(BaseEvent):
    type: str = "sites_info"
    sources: list[SitesInfo]


class BaseSource(BaseModel):
    model_config = ConfigDict(frozen=True)
    text: str
    url: str


class Source(BaseSource):
    title: str
    step_id: int | None = None

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, value):
        return isinstance(value, Source) and self.url == value.url


class Fact(BaseSource):
    text: Annotated[str, Field(description=Prompts.FACT)]
    url: Annotated[str, Field(description=Prompts.URL)]


class Facts(AskSchema):
    facts: list[Fact]


class AgentState(BaseModel):
    question: str
    step_count: int = 0
    max_steps: int = 4
    facts: Annotated[list[Fact], Field(default_factory=list)]
    sourses: Annotated[set[Source], Field(default_factory=set)]
    queries: Annotated[set[str], Field(default_factory=set)]
    images: Annotated[list[str], Field(default_factory=list, max_length=4)]


class NeedMoreDataEvent(BaseEvent):
    type: str = "need_more_data"
    reason: str
    new_queries: list[str]


class ChatNameEvent(BaseEvent):
    type: str = "chat_name"
    name: str


class ChatIdEvent(BaseEvent):
    type: str = "chat_id"
    chat_id: str


class PhotoEvent(BaseEvent):
    type: str = "photos"
    photos: list[str]


class TokenEvent(BaseEvent):
    type: str = "token"
    token: str


class SearchResult(BaseModel):
    sources: list[Source]
    photos: list[str]

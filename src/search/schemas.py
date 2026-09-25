from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


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


class BaseEvent(BaseModel):
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
    sites: list[Sourse]
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


class FinalResponseEvent(BaseEvent):
    type: str = "final_answer_chunk"
    text: str


class Sourse(BaseModel):
    url: str


class Fact(BaseModel):
    text: str
    url: str
    step: int


class AgentState(BaseModel):
    question: str
    step_count: int | None
    max_steps: int = 4
    facts: Annotated[list[Fact], Field(default_factory=list)]
    sourses: Annotated[set[Sourse], Field(default_factory=set)]
    queries: Annotated[set[str], Field(default_factory=set)]


class ReflectionDecision(BaseModel):
    is_sufficient: bool
    reasoning: str
    new_search_queries: Annotated[list[str], Field(default_factory=list)]


class Source(BaseModel):
    model_config = ConfigDict(frozen=True)
    text: str
    url: str

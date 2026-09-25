# src/search/registry.py
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from typing import Any

from src.llm.schemas import (
    AskSchema,
    QueriesSchema,
    ResponseSchema,
    SerperSchema,
    TavilySchema,
)
from src.search.base import BaseSearch
from src.search.providers.searxng import searxng_client
from src.search.providers.serper import serper_client
from src.search.providers.tavily import tavily_client
from src.search.schemas import (
    SearchSchema,
    Source,
)

from .utils import (
    build_searxng_schema,
    build_serper_schema,
    build_tavily_schema,
    process_links,
    process_tavily,
)


@dataclass(slots=True)
class ProviderConfig[T: AskSchema]:
    schema: type[T]
    builder: Callable[[str, T], SearchSchema]
    client: BaseSearch[Any, Any]
    process: Callable[
        [Sequence[ResponseSchema], ResponseSchema], Awaitable[list[Source]]
    ]


providers: dict[str, ProviderConfig[Any]] = {
    "searxng": ProviderConfig(
        QueriesSchema, build_searxng_schema, searxng_client, process_links
    ),
    "serper": ProviderConfig(
        SerperSchema, build_serper_schema, serper_client, process_links
    ),
    "tavily": ProviderConfig(
        TavilySchema, build_tavily_schema, tavily_client, process_tavily
    ),
}

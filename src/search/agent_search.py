import asyncio
from collections.abc import AsyncGenerator

from fastapi import Request

from src.llm.base import llm
from src.llm.schemas import AskSchema
from src.matcher.match import match_results
from src.search.registry import ProviderConfig

from .schemas import (
    AgentState,
    Fact,
    ReflectionDecision,
)

MAX_FACTS_COUNT = 40


async def search_data[T: AskSchema](q: str, config: ProviderConfig[T]):
    query = await llm.get_query(q, config.schema)
    schema = config.builder(q, query)
    links_results, photos_results = await config.client.search(schema)
    process_result = await config.process(links_results, photos_results)
    match_result = await asyncio.to_thread(match_results, q, process_result)
    return match_result


async def reflection_decision(state: AgentState) -> ReflectionDecision: ...


async def get_facts(quries: list[str]) -> list[Fact]: ...


async def stream_response(state: AgentState) -> AsyncGenerator[str, None]: ...


async def agent_search[T: AskSchema](
    q: str, config: ProviderConfig[T], request: Request
) -> AsyncGenerator[str, None]: ...

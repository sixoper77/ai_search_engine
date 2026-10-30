import asyncio
import traceback
from collections.abc import AsyncGenerator, Sequence
from uuid import UUID

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Message, Role
from src.db.requests import put_message_in_chat
from src.llm.base import llm
from src.llm.enums import Prompts
from src.llm.schemas import AskSchema, ReflectionDecision
from src.matcher.match import match_results
from src.search.registry import ProviderConfig
from src.search.schemas import Facts

from .schemas import (
    AgentState,
    ChatIdEvent,
    DoneEvent,
    ErrorEvent,
    InfoEvent,
    NeedMoreDataEvent,
    PhotoEvent,
    SearchResult,
    SitesInfo,
    SitesInfoEvent,
    Source,
    StepSrtartEvent,
    TokenEvent,
)
from .utils import emit, parse_chat_history

MAX_FACTS_COUNT = 40


async def search_data[T: AskSchema](
    q: str, config: ProviderConfig[T], step_number: int
) -> SearchResult:
    query = await llm.get_query(q, schema=config.schema)
    schema = config.builder(q, query)
    links_results, photos_results = await config.client.search(schema)
    process_result = await config.process(links_results, photos_results)
    match_result = await asyncio.to_thread(
        match_results, q, process_result, step_number
    )
    print(type(photos_results), photos_results)
    return SearchResult(sources=match_result, photos=photos_results)


async def reflection_decision(state: AgentState) -> ReflectionDecision:
    question = state.question
    facts = "\n".join(f"{f.text}-{f.url}" for f in state.facts)
    combined_prompt = f"Data:\n{facts}\n\nUser Question:\n{question}"
    decision = await llm.get_query(
        combined_prompt, Prompts.DECISION, schema=ReflectionDecision
    )
    return decision


async def get_facts(state: AgentState, data: list[Source]) -> Facts:
    question = state.question
    text = " ".join(t.text for t in data)
    sources = "\n".join(f"{s.url} - {s.title}" for s in data)
    combined_prompt = (
        f"Data:\n{text}\n\nSources:\n{sources}\n\nUser Question:\n{question}"
    )
    facts = await llm.get_query(combined_prompt, Prompts.FACTS, schema=Facts)
    state.facts.extend(facts.facts)
    return facts


async def stream_response(state: AgentState) -> AsyncGenerator[str, None]:
    query, sources = state.question, state.facts

    async for token in llm.astream(query, sources):
        yield token


async def agent_search[T: AskSchema](
    q: str,
    config: ProviderConfig[T],
    request: Request,
    session: AsyncSession,
    chat_id: UUID,
    history: Sequence[Message],
) -> AsyncGenerator[str, None]:
    q_with_history = parse_chat_history(q, history) if history else None
    state = AgentState(question=q_with_history if q_with_history else q)
    pending_queries = [q_with_history if q_with_history else q]
    parts = []
    try:
        if await request.is_disconnected():
            return
        yield emit(ChatIdEvent(chat_id=str(chat_id)))
        while state.step_count < state.max_steps:
            if await request.is_disconnected():
                return
            state.step_count += 1
            yield emit(
                StepSrtartEvent(
                    messgae="Начинаю поиск..."
                    if state.step_count == 1
                    else "Ищу дополнительные данные...",
                    step=state.step_count,
                )
            )
            try:
                async with asyncio.TaskGroup() as tg:
                    tasks = [
                        tg.create_task(search_data(qs, config, state.step_count))
                        for qs in pending_queries
                    ]
                sources = [task.result() for task in tasks]
                queries = [s for sr in sources for s in sr.sources]
                photos = [p for ph in sources for p in ph.photos]
                for p in photos:
                    if p not in state.images and len(state.images) < 4:
                        state.images.append(p)
                print(queries)
            except Exception as e:
                traceback.print_exception(e)
                yield emit(
                    ErrorEvent(message="Не удалось выполнить поиск", recoverable=False)
                )
                return
            if not queries:
                yield emit(
                    ErrorEvent(
                        message="Не удалось получить поисковые запросы",
                        recoverable=False,
                    )
                )
                return
            state.sourses.update(set(queries))

            yield emit(
                SitesInfoEvent(
                    sources=[SitesInfo(url=u.url, title=u.title) for u in queries]
                )
            )
            yield emit(InfoEvent(message="Создаю факты..."))
            await get_facts(state, queries)
            decision = await reflection_decision(state)
            if decision.is_sufficient:
                yield emit(
                    DoneEvent(
                        total_steps=state.step_count,
                        total_sources=len(state.sourses),
                        message=decision.reasoning,
                    )
                )
                break
            else:
                pending_queries = decision.new_search_queries
                yield emit(
                    NeedMoreDataEvent(
                        reason=decision.reasoning,
                        new_queries=decision.new_search_queries,
                    )
                )

        try:
            yield emit(PhotoEvent(photos=state.images[:4]))
            async for chunk in stream_response(state):
                parts.append(chunk)
                yield emit(TokenEvent(token=chunk))
                await asyncio.sleep(0)
        finally:
            text = "".join(parts)
            if text:
                await put_message_in_chat(session, chat_id, q, Role.USER)
                await put_message_in_chat(
                    session, chat_id, text, Role.AI, list(dict.fromkeys(state.sourses))
                )
                await session.commit()

    except Exception as e:
        print(e)

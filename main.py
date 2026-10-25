# This code is dirty and it isn't final yet
from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base, Chat, Role
from src.db.requests import (
    async_session,
    engine,
    get_db,
    get_or_create,
    put_message_in_chat,
    set_title_if_none,
)
from src.llm.base import llm
from src.llm.enums import Prompts
from src.llm.schemas import (
    AskSchema,
    ChatName,
)
from src.matcher.match import match_results
from src.search.agent_search import agent_search
from src.search.registry import ProviderConfig, providers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


async def get_chat(session: SessionDep, chat_id: UUID | None = None):
    chat, is_new = await get_or_create(session, chat_id)
    await session.commit()
    return chat, is_new


app = FastAPI(lifespan=lifespan)

SessionDep = Annotated[AsyncSession, Depends(get_db)]
ChatDep = Annotated[tuple[Chat, bool], Depends(get_chat)]


tasks_stor: set[asyncio.Task] = set()


async def set_title(chat_id: UUID, q: str) -> None:
    title = await llm.get_query(q, Prompts.NAME, schema=ChatName)
    async with async_session() as session:
        await set_title_if_none(session, chat_id, title.name)


async def generate_and_save_title(chat_info: ChatDep, q: str) -> None:
    chat, is_new = chat_info
    if not is_new:
        return
    task = asyncio.create_task(set_title(chat.id, q))
    tasks_stor.add(task)
    task.add_done_callback(tasks_stor.discard)


async def default_search[T: AskSchema](
    q: str,
    config: ProviderConfig[T],
    request: Request,
    session: AsyncSession,
    chat_id: UUID,
) -> AsyncGenerator[str, Any]:
    parts = []
    query = await llm.get_query(q, schema=config.schema)
    schema = config.builder(q, query)
    links_results, photos_results = await config.client.search(schema)
    process_result = await config.process(links_results, photos_results)
    match_result = await asyncio.to_thread(match_results, q, process_result)
    try:
        async for token in llm.astream(q, match_result):
            parts.append(token)
            yield token
    finally:
        text = "".join(parts)
        if text:
            await put_message_in_chat(session, chat_id, q, Role.USER)
            await put_message_in_chat(session, chat_id, text, Role.AI, match_result)
            await session.commit()


@app.get("/search/", dependencies=[Depends(generate_and_save_title)])
async def pro_search(
    q: str,
    provider_name: str,
    pro_search: bool,
    request: Request,
    chat_info: ChatDep,
    session: SessionDep,
):
    chat, _ = chat_info
    chat_id = chat.id
    config = providers.get(provider_name)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The query was entered incorrectly, or such a provider does not exist.",
        )
    if q is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="The query is empty"
        )
    if await request.is_disconnected():
        return
    search_type = agent_search if pro_search else default_search
    return StreamingResponse(
        search_type(q, config, request, session, chat_id),
        media_type="text/event-stream",
    )

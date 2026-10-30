from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
import sys
from typing import Annotated, Any
from uuid import UUID

# Ensure backend root is on sys.path so 'src' and 'config' resolve cleanly
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src.db.models import Base, Chat, Message, Role
from src.db.requests import (
    async_session,
    engine,
    get_chat_history,
    get_chat_list,
    get_db,
    get_or_create,
    put_message_in_chat,
    set_title_if_none,
)
from src.db.schemas import ChatItem, MessageOut
from src.llm.base import llm
from src.llm.enums import Prompts
from src.llm.schemas import (
    AskSchema,
    ChatName,
)
from src.matcher.match import match_results
from src.search.agent_search import agent_search
from src.search.registry import ProviderConfig, providers
from src.search.schemas import ChatIdEvent, PhotoEvent, TokenEvent
from src.search.utils import emit, parse_chat_history


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="AI Search Engine API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Chat-Id"],
)

SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_chat(session: SessionDep, chat_id: UUID | None = None):
    chat, is_new = await get_or_create(session, chat_id)
    await session.commit()
    return chat, is_new


ChatDep = Annotated[tuple[Chat, bool], Depends(get_chat)]

tasks_stor: set[asyncio.Task] = set()


async def set_title(chat_id: UUID, q: str) -> None:
    try:
        title = await llm.get_query(q, Prompts.NAME, schema=ChatName)
        async with async_session() as session:
            await set_title_if_none(session, chat_id, title.name)
    except Exception as e:
        print(f"Error generating chat title: {e}")


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
    history: Sequence[Message],
) -> AsyncGenerator[str, Any]:
    if await request.is_disconnected():
        return
    parts = []
    if history:
        question = parse_chat_history(q, history)
        query = await llm.get_query(question, schema=config.schema)
    else:
        question = q
        query = await llm.get_query(q, schema=config.schema)

    schema = config.builder(q, query)
    links_results, photos_results = await config.client.search(schema)
    process_result = await config.process(links_results, photos_results)
    match_result = await asyncio.to_thread(match_results, q, process_result)
    try:
        yield emit(ChatIdEvent(chat_id=str(chat_id)))
        yield emit(PhotoEvent(photos=photos_results[:4]))
        async for token in llm.astream(question, match_result):
            parts.append(token)
            yield emit(TokenEvent(token=token))
            await asyncio.sleep(0)
    finally:
        text = "".join(parts)
        if text:
            await put_message_in_chat(session, chat_id, q, Role.USER)
            await put_message_in_chat(session, chat_id, text, Role.AI, match_result)
            await session.commit()


@app.get("/search/", dependencies=[Depends(generate_and_save_title)])
async def pro_search(
    q: str,
    request: Request,
    chat_info: ChatDep,
    session: SessionDep,
    provider_name: str | None = None,
    pro_search: bool = False,
):
    chat, _ = chat_info
    chat_id = chat.id
    history = await get_chat_history(session, chat_id)

    if not provider_name:
        default_prov = settings.get_provider()
        provider_name = default_prov[0] if default_prov else "tavily"

    config = providers.get(provider_name)
    if config is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The query was entered incorrectly, or provider '{provider_name}' does not exist.",
        )
    if not q or not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The query is empty"
        )
    if await request.is_disconnected():
        return
    search_type = agent_search if pro_search else default_search
    return StreamingResponse(
        search_type(q, config, request, session, chat_id, history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "X-Chat-Id": str(chat_id),
        },
    )


@app.get("/chats/", response_model=list[ChatItem])
async def chat_list(
    session: SessionDep,
    before_updated_at: datetime | None = None,
    before_id: UUID | None = None,
):
    cursor = (before_updated_at, before_id) if before_id and before_updated_at else None
    return await get_chat_list(session, cursor)


@app.get("/chat/{id}", response_model=list[MessageOut])
async def load_chat_history(id: UUID, session: SessionDep):
    return await get_chat_history(session, id)


@app.get("/providers/")
async def get_providers_list():
    active_prov = settings.get_provider()
    default_name = active_prov[0] if active_prov else "tavily"
    return {
        "providers": list(providers.keys()),
        "default": default_name,
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}

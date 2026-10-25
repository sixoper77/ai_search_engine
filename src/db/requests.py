from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings
from src.search.schemas import Source

from .models import Chat, Message, Role, StepSource

engine = create_async_engine(settings.database_url, pool_pre_ping=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_chat(session: AsyncSession, chat_id: UUID) -> Chat | None:
    query = await session.execute(select(Chat).where(Chat.id == chat_id))
    return query.scalar_one_or_none()


async def get_or_create(
    session: AsyncSession, chat_id: UUID | None
) -> tuple[Chat, bool]:
    if chat_id is None:
        chat = Chat()
        session.add(chat)
        await session.flush()
        return chat, True
    chat = await session.get(Chat, chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat does not exist"
        )
    return chat, False


async def set_title_if_none(session: AsyncSession, chat_id: UUID, title: str) -> None:
    await session.execute(
        update(Chat).where(Chat.id == chat_id, Chat.name.is_(None)).values(name=title)
    )
    await session.commit()


async def put_message_in_chat(
    session: AsyncSession,
    chat_id: UUID,
    message: str,
    role: Role,
    steps: list[Source] | None = None,
):
    msg = Message(
        chat_id=chat_id,
        role=role,
        content=message,
        steps=[
            StepSource(title=s.title, url=s.url, step_number=s.step_id) for s in steps
        ]
        if steps
        else [],
    )
    session.add(msg)
    await session.flush()
    return msg

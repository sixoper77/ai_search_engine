from collections.abc import AsyncGenerator, Sequence
from datetime import datetime
from uuid import UUID

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import and_, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import selectinload

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
    await session.execute(
        update(Chat).where(Chat.id == chat_id).values(updated_at=func.now())
    )
    await session.flush()
    return msg


async def get_chat_list(
    session: AsyncSession,
    cursor: tuple[datetime, UUID] | None = None,
    limit: int = 20,
):
    stmt = select(Chat.id, Chat.name, Chat.updated_at).order_by(
        Chat.updated_at.desc(), Chat.id.desc()
    )

    if cursor is not None:
        last_dt, last_id = cursor
        stmt = stmt.where(
            or_(
                Chat.updated_at < last_dt,
                and_(Chat.updated_at == last_dt, Chat.id < last_id),
            )
        )
    result = await session.execute(stmt.limit(limit))
    return result.all()


async def get_chat_history(session: AsyncSession, chat_id: UUID) -> Sequence[Message]:
    chat = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .options(selectinload(Message.steps))
        .order_by(Message.id)
    )
    result = await session.scalars(chat)
    return result.all()

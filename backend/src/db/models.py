from datetime import datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Enum, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class Role(StrEnum):
    AI = "ai"
    USER = "user"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str | None] = mapped_column(index=True, default=None)
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chat",
        order_by="Message.id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[intpk]
    chat_id: Mapped[UUID] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"),
        index=True,
    )
    role: Mapped[Role] = mapped_column(
        Enum(
            Role,
            name="message_role",
            native_enum=False,
            create_constraint=True,
            validate_strings=True,
        )
    )
    content: Mapped[str]
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    steps: Mapped[list["StepSource"]] = relationship(
        back_populates="message",
        order_by="StepSource.step_number, StepSource.id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class StepSource(Base):
    __tablename__ = "step_source"
    __table_args__ = (
        CheckConstraint("step_number BETWEEN 1 AND 4", name="ck_step_number_range"),
    )

    id: Mapped[intpk]
    title: Mapped[str]
    url: Mapped[str]
    step_number: Mapped[int | None] = mapped_column(default=None)
    message_id: Mapped[int] = mapped_column(
        ForeignKey("messages.id", ondelete="CASCADE"),
        index=True,
    )
    message: Mapped["Message"] = relationship(back_populates="steps")

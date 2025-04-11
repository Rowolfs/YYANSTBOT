from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Boolean, DateTime, Integer
from typing import Optional, List
from datetime import datetime
from config import Base

class ScheduleBase(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    users: Mapped[List["UserScheduleBase"]] = relationship("UserScheduleBase", back_populates="schedule", cascade="all, delete")
    slots: Mapped[List["SlotBase"]] = relationship("SlotBase", back_populates="schedule", cascade="all, delete")


class ChatScheduleBase(Base):
    __tablename__ = "chats_schedules"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id", ondelete="CASCADE"), primary_key=True)


class UserScheduleBase(Base):
    __tablename__ = "users_schedules"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id", ondelete="CASCADE"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    schedule: Mapped["ScheduleBase"] = relationship("ScheduleBase", back_populates="users")
    user: Mapped["UserBase"] = relationship("UserBase", back_populates="schedules")


class SlotBase(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    schedule_id: Mapped[int] = mapped_column(ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False)
    time_start: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    time_end: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    schedule: Mapped["ScheduleBase"] = relationship("ScheduleBase", back_populates="slots")
    users: Mapped[List["UserSlotBase"]] = relationship("UserSlotBase", back_populates="slot", cascade="all, delete")


class UserSlotBase(Base):
    __tablename__ = "users_slots"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    slot_id: Mapped[int] = mapped_column(ForeignKey("slots.id", ondelete="CASCADE"), primary_key=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    booking_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["UserBase"] = relationship("UserBase", back_populates="slots")
    slot: Mapped["SlotBase"] = relationship("SlotBase", back_populates="users")


class RepeatBase(Base):
    __tablename__ = "repeats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slot_id: Mapped[Optional[int]] = mapped_column(ForeignKey("slots.id", ondelete="CASCADE"), nullable=True)
    schedule_id: Mapped[Optional[int]] = mapped_column(ForeignKey("schedules.id", ondelete="CASCADE"), nullable=True)
    chat_id: Mapped[Optional[int]] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    start: Mapped[DateTime] = mapped_column(DateTime)
    end: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    interval: Mapped[Optional[int]] = mapped_column(Integer)
    day: Mapped[Optional[Boolean]] = mapped_column(Boolean)
    year: Mapped[Optional[Boolean]] = mapped_column(Boolean)
    week: Mapped[Optional[int]] = mapped_column(Integer)
    month: Mapped[Optional[int]] = mapped_column(Integer)

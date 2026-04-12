from sqlalchemy import ForeignKey, BigInteger, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class User(Base):
    '''Telegram user'''
    __tablename__ = "Users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str | None] = mapped_column(String(50), nullable=True)

    balance: Mapped[int] = mapped_column(Integer, default=0)

    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    subs: Mapped[list["Subscription"]] = relationship(back_populates="user")


class Subscription(Base):
    pass
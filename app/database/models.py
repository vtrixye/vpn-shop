from sqlalchemy import String, Integer, BigInteger, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import ARRAY, UUID
import enum
import uuid as uuid_lib

class Base(DeclarativeBase):
    pass

class User(Base):
    """Telegram user"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str | None] = mapped_column(String(50), nullable=True)

    balance: Mapped[int] = mapped_column(Integer, default=0)

    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    trial: Mapped[bool] = mapped_column(Boolean, default=True)

    subscriptions: Mapped[List["Subscription"]] = relationship("Subscription", back_populates="user")
    payments: Mapped[List["Payment"]] = relationship("Payment", back_populates="user")

class Subscription(Base):
    """Remnawave user"""

    __tablename__ = "subscriptions"

    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid_lib.uuid4
    )
    short_uuid: Mapped[str] = mapped_column(String(36), unique=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    status: Mapped[str] = mapped_column(String(20))

    traffic_limit_bytes: Mapped[int] = mapped_column(BigInteger, default=0)
    traffic_limit_strategy: Mapped[str] = mapped_column(String(50))

    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tag: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    hwid_device_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime)

    subscription_url: Mapped[str] = mapped_column(String(500))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")

    squads: Mapped[list[uuid_lib.UUID]] = mapped_column(
        ARRAY(UUID(as_uuid=True), dimensions=1),
        default=list
    )

class PaymentType(str, enum.Enum):
    DEPOSIT = "deposit"
    SUB_PURCHASE = "sub_purchase"
    SUB_RENEWAL = "sub_renewal"
    ADD_DEVICE = "add_device"
    REFUND = "refund"
    WITHDRAWAL = "withdrawal"
    ADMIN_ADJUSTMENT = "admin_adjustment"

class PaymentMethod(str, enum.Enum):
    Platega = "Platega"
    CryptoBot = "CryptoBot"
    TelegramStars = "TelegramStars"
    Balance = "Balance"

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="payments")

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False)

    type: Mapped[PaymentType] = mapped_column(Enum(PaymentType), nullable=True)
    method: Mapped[PaymentMethod] = mapped_column(Enum(PaymentMethod), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime)
    
    data: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=dict, nullable=True)
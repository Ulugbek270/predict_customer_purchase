import datetime
from core.base import Base
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime


class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str]

    requirement_items = relationship("RequirementGoods", back_populates="goods")


class ClientLocal(Base):
    __tablename__ = "clients_local"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_ru: Mapped[str]
    phone: Mapped[str | None]
    email: Mapped[str | None]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    requirements = relationship("Requirement", back_populates="client")


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True)


    full_name: Mapped[str]
    phone: Mapped[str | None]
    email: Mapped[str | None]


    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    requirements = relationship("Requirement", back_populates="agent")


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id", ondelete="CASCADE")
    )
    client_local_id: Mapped[int] = mapped_column(
        ForeignKey("clients_local.id", ondelete="CASCADE")
    )
    date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    agent = relationship("Agent", back_populates="requirements")
    client = relationship("ClientLocal", back_populates="requirements")
    items = relationship("RequirementGoods", back_populates="requirement")


class RequirementGoods(Base):
    __tablename__ = "requirement_goods"

    id: Mapped[int] = mapped_column(primary_key=True)
    requirement_id: Mapped[int] = mapped_column(
        ForeignKey("requirements.id", ondelete="CASCADE")
    )
    goods_id: Mapped[int] = mapped_column(
        ForeignKey("goods.id", ondelete="CASCADE")
    )
    amount: Mapped[float]
    cost_sell: Mapped[float]

    requirement = relationship("Requirement", back_populates="items")
    goods = relationship("Goods", back_populates="requirement_items")
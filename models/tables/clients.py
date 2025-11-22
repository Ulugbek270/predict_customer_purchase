import datetime
from core.base import Base
from sqlalchemy import  func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    contact_name: Mapped[str | None]
    phone: Mapped[str | None]
    email: Mapped[str | None]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    orders = relationship("Order", back_populates="client")
    customers = relationship("Customer", back_populates="client")

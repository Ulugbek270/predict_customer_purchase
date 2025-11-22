import datetime
from core.base import Base
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    order_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    total_amount: Mapped[float]
    client = relationship("Client", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

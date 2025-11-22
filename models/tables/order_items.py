from core.base import Base

from sqlalchemy import  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship




class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    goods_id: Mapped[int] = mapped_column(ForeignKey("goods.id", ondelete="CASCADE"))
    quantity: Mapped[float]
    price_at_time: Mapped[float]

    order = relationship("Order", back_populates="items")
    goods = relationship("Goods", back_populates="items")

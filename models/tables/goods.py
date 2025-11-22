
import datetime
from core.base import Base
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime




class Goods(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    unit: Mapped[str]               # kg, pcs, etc.
    price: Mapped[float]
    is_active: Mapped[bool] = mapped_column(default=True)

    items = relationship("OrderItem", back_populates="goods")

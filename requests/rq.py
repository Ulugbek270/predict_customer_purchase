from collections import defaultdict
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models.schemas.schemas import OrderSchema
from models.tables.orders import Order
from models.tables.order_items import OrderItem
from core.conn import connection
from sqlalchemy import select

@connection
async def get_all_orders(session):
    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.goods)  # load goods for each item
        )
        .order_by(Order.id)
    )
    orders = result.scalars().all()
    return [OrderSchema.model_validate(q, from_attributes=True) for q in orders]


@connection
async def get_purchase_patterns(
        session: AsyncSession,
        min_orders: int = 3,
        active_only: bool = True
) -> dict:
    """
    Fetch all orders with items and group by client-product combinations
    Returns: dict[client_id][goods_id] = {dates, quantities, client, goods}
    """
    # Fetch all orders with related data
    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.client),
            selectinload(Order.items).selectinload(OrderItem.goods)
        )
        .order_by(Order.order_date)
    )
    orders = result.scalars().all()

    # Group by client and goods
    patterns = defaultdict(lambda: defaultdict(lambda: {
        "dates": [],
        "quantities": [],
        "client": None,
        "goods": None
    }))

    for order in orders:
        client_id = order.client_id
        client = order.client

        for item in order.items:
            goods_id = item.goods_id
            goods = item.goods

            # Skip inactive goods if filtering
            if active_only and not goods.is_active:
                continue

            # Store pattern data
            pattern = patterns[client_id][goods_id]
            pattern["dates"].append(order.order_date)
            pattern["quantities"].append(item.quantity)
            pattern["client"] = client
            pattern["goods"] = goods

    return patterns
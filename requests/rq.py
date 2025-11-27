from collections import defaultdict
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from models.schemas.schemas import RequirementSchema
from models.tables.tables_all import Requirement, RequirementGoods, Goods
from core.conn import connection
from sqlalchemy import select

@connection
async def get_all_requirements(session):
    result = await session.execute(
        select(Requirement)
        .options(
            selectinload(Requirement.agent),
            selectinload(Requirement.items).selectinload(RequirementGoods.goods),
        )
        .order_by(Requirement.id)
    )
    requirements = result.scalars().all()
    return [RequirementSchema.model_validate(req, from_attributes=True) for req in requirements]


@connection
async def get_purchase_patterns(
        session: AsyncSession,
        min_requirements: int = 3,
) -> dict:
    """
    Analyze purchase patterns by grouping requirements by client and goods.
    Returns patterns with dates, quantities, and related entities.
    """
    result = await session.execute(
        select(Requirement)
        .options(
            selectinload(Requirement.client),
            selectinload(Requirement.agent),
            selectinload(Requirement.items).selectinload(RequirementGoods.goods)
        )
        .order_by(Requirement.date)
    )
    requirements = result.scalars().all()

    # Group by client and goods
    patterns = defaultdict(lambda: defaultdict(lambda: {
        "dates": [],
        "amount": [],
        "prices": [],
        "client": None,
        "goods": None
    }))

    for requirement in requirements:
        client_id = requirement.client_local_id
        client = requirement.client

        for item in requirement.items:
            goods_id = item.goods_id
            goods = item.goods

            # Store pattern data
            pattern = patterns[client_id][goods_id]
            pattern["dates"].append(requirement.date)
            pattern["amount"].append(item.amount)
            pattern["prices"].append(item.cost_sell)
            pattern["client"] = client
            pattern["goods"] = goods

    # Filter patterns by minimum requirement count
    filtered_patterns = defaultdict(dict)
    for client_id, goods_dict in patterns.items():
        for goods_id, pattern in goods_dict.items():
            if len(pattern["dates"]) >= min_requirements:
                filtered_patterns[client_id][goods_id] = pattern

    return filtered_patterns
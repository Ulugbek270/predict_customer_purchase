from typing import List

import requests.rq as rq
from models.schemas.schemas import (
    OrderSchema
)

from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=List[OrderSchema])
async def get_all_orders():
    return await rq.get_all_orders()


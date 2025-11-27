from typing import List

import requests.rq as rq
from models.schemas.schemas import (
    RequirementSchema
)

from fastapi import APIRouter, HTTPException, Path

router = APIRouter(prefix="/requirements", tags=["Requirements"])


@router.get("/", response_model=List[RequirementSchema])
async def get_all_req():
    return await rq.get_all_requirements()


from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class GoodsSchema(BaseModel):
    id: int
    name_en: str

    model_config = dict(from_attributes=True)


class RequirementGoodsSchema(BaseModel):
    id: int
    goods: GoodsSchema
    amount: float
    cost_sell: float

    model_config = dict(from_attributes=True)


class AgentSchema(BaseModel):
    id: int
    full_name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime

    model_config = dict(from_attributes=True)


class RequirementSchema(BaseModel):
    id: int
    agent_id: int
    client_local_id: int
    date: datetime
    agent: Optional[AgentSchema] = None
    items: Optional[List[RequirementGoodsSchema]] = None

    model_config = dict(from_attributes=True)


class ClientLocalSchema(BaseModel):
    id: int
    name_ru: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    agents: List[AgentSchema] = []
    requirements: List[RequirementSchema] = []

    model_config = dict(from_attributes=True)


class PredictionSchema(BaseModel):
    client_id: int
    client_name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    goods_id: int
    goods_name: str
    last_requirement_date: datetime
    days_since_last_requirement: int
    average_cycle_days: float
    cycle_variance: float
    confidence_score: float
    predicted_amount: float
    requirement_count: int

    model_config = dict(from_attributes=True)


class PredictionsResponse(BaseModel):
    predictions: List[PredictionSchema]
    generated_at: datetime
    total_predictions: int

    model_config = dict(from_attributes=True)
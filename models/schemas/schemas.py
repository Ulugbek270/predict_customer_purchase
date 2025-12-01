from typing import List, Optional
from datetime import datetime, date
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



class SalesSchema(BaseModel):
    sales_id: int
    sales_number: str
    client_id: int
    agent_id: int
    created_date: date
    paid_date: Optional[date] = None  # In case it can be NULL

    model_config = dict(from_attributes=True)

class ClientLocalSchema(BaseModel):
    id: int
    name_ru: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    agents: List[AgentSchema] = []
    requirements: List[SalesSchema] = []

    model_config = dict(from_attributes=True)


from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import List, Optional


class PredictionSchema(BaseModel):
    # Client & Product Info
    client_id: int
    client_name: str
    agent_id: int
    agent_name: str
    goods_id: int
    goods_name: str

    # Pattern Analysis
    requirement_count: int = Field(..., description="Number of purchases analyzed")
    purchase_count: int = Field(..., description="Total purchases in pattern")

    # Dates
    last_requirement_date: date
    days_since_last_requirement: int
    predicted_next_purchase_date: date

    # Pattern Metrics
    average_cycle_days: float = Field(..., alias="avg_interval_days")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    pattern_consistency: str = Field(...,
                                     description="Pattern regularity: highly_regular, regular, somewhat_regular, irregular")

    # Amount Predictions
    predicted_amount: float

    class Config:
        populate_by_name = True


class PredictionsResponse(BaseModel):
    predictions: List[PredictionSchema]
    generated_at: datetime
    total_predictions: int
    filters_applied: dict = Field(default_factory=dict)
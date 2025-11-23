from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class GoodsSchema(BaseModel):
    id: int
    name: str
    unit: str
    price: float
    is_active: bool

    model_config = dict(from_attributes=True)


class OrderItemSchema(BaseModel):
    id: int
    goods: GoodsSchema
    quantity: float
    price_at_time: float

    model_config = dict(from_attributes=True)

class OrderSchema(BaseModel):
    id: int
    client_id: int
    order_date: datetime
    total_amount: float
    items: Optional[List[OrderItemSchema]] = None

    model_config = dict(from_attributes=True)


class CustomerSchema(BaseModel):
    id: int
    client_id: int
    full_name: str
    phone: Optional[str]
    email: Optional[str]

    model_config = dict(from_attributes=True)

# Client schema
class ClientSchema(BaseModel):
    id: int
    name: str
    contact_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    created_at: datetime
    customers: List[CustomerSchema] = []
    orders: List[OrderSchema] = []

    model_config = dict(from_attributes=True)


class PredictionSchema(BaseModel):
    client_id: int
    client_name: str
    contact_name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    goods_id: int
    goods_name: str
    unit: str
    last_order_date: datetime
    days_since_last_order: int
    average_cycle_days: float
    cycle_variance: float
    confidence_score: float
    predicted_quantity: float
    order_count: int  # Total number of orders for this client-product

    class Config:
        from_attributes = True


class PredictionsResponse(BaseModel):
    predictions: List[PredictionSchema]
    generated_at: datetime
    total_predictions: int


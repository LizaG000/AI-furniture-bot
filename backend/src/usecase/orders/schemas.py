from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from datetime import datetime


class OrderProductSchema(BaseModel):
    id: UUID
    name: str
    count: int
    price: float
    discount: float


class ReturnOrderSchema(BaseModel):
    order_id: UUID
    created_at: datetime
    address: Optional[str]
    user_full_name: Optional[str]
    products: List[OrderProductSchema]
    total_price: float

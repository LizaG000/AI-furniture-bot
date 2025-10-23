from src.application.schemas.common import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class CreateOrdersSchema(BaseModel):
    id_user: int
    id_product: UUID
    id_addresses: UUID
    status: str

class OrdersSchema(CreateOrdersSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

class CreateOrdersProductsSchemas(BaseModel):
    id_order: UUID
    id_product: UUID
    count: int
    price: float
    discount: float


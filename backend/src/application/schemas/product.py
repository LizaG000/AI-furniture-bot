from src.application.schemas.common import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class CreateProductSchema(BaseModel):
    name: str
    description: str
    price: float
    count: int
    discount: float
    length: float
    height: float
    width: float
    id_category: UUID
    images: List[str] = []

class ProductSchema(CreateProductSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


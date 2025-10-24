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

class UpdateProductSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    count: int | None = None
    discount: float | None = None
    length: float | None = None
    height: float | None = None
    width: float | None = None
    id_category: UUID | None = None
    images: List[str] | None = None


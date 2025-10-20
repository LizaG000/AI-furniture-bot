from pydantic import BaseModel
from typing import List
from uuid import UUID

class ProductCreateSchema(BaseModel):
    name: str
    description: str
    price: float
    count: int
    discount: float
    length: float
    height: float
    width: float
    id_category: UUID
    colors: List[str] = []
    materials: List[str] = []
    photos: List[str] = []

class ProductBatchCreateSchema(BaseModel):
    products: List[ProductCreateSchema]

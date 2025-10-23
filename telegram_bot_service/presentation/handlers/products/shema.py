from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from pydantic import TypeAdapter
from typing import List

@dataclass
class ProductSchema(BaseModel):
    id: UUID  = Field(..., alias="id")
    name: str  = Field(..., alias="name")
    description: str  = Field(..., alias="description")
    price: float  = Field(..., alias="price")
    count: int  = Field(..., alias="count")
    discount: float  = Field(..., alias="discount")
    length: float  = Field(..., alias="length")
    height: float  = Field(..., alias="height")
    width: float  = Field(..., alias="width")
    category: str  = Field(..., alias="category")
    images: list[str]  = Field(..., alias="images")
    colors: list[str]  = Field(..., alias="colors")
    materials: list[str]  = Field(..., alias="materials")


adapter = TypeAdapter(List[ProductSchema])
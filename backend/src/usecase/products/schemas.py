from pydantic import BaseModel
from uuid import UUID


class CreateProductBatchSchema(BaseModel):
    name: str
    description: str
    price: float
    count: int
    discount: float
    length: float
    height: float
    width: float
    category_name: str
    images: list[str] = []
    colors: list[str] = []
    materials: list[str] = []


class GetProductsSchema(BaseModel):
    categories: list[str]|None = []
    colors: list[str]|None = []
    materials: list[str]|None = []

class ReturnProductsSchema(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    count: int
    discount: float
    length: float
    height: float
    width: float
    category: str
    images: list[str] = []
    colors: list[str]
    materials: list[str]
    

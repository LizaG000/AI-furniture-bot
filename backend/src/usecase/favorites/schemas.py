from pydantic import BaseModel
from uuid import UUID

class GetFavoritesSchema(BaseModel):
    id_user: int

class ReturnFavoritesSchema(BaseModel):
    id: UUID
    id_user: int
    id_product: UUID
    name: str
    description: str
    price: float
    count: int
    discount: float
    length: float
    height: float
    width: float
    category: str
    images: list[str]
    colors: list[str]
    materials: list[str]
    

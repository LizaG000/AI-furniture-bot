from pydantic import BaseModel
from src.application.schemas.product import CreateProductSchema

class CreateProductBatchSchema(BaseModel):
    name: str
    description: str
    price: float
    count: int
    discount: float
    length: float
    height: float
    width: float
    id_category: str
    images: list[str] = []
    colors: list[str] = []
    materials: list[str] = []


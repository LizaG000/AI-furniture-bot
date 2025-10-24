from pydantic import BaseModel
from uuid import UUID

class AddProductsSchema(BaseModel):
    id_product: UUID
    count: int
    price: float
    discount: float


class AddOrdersProductsSchema(BaseModel):
    id_user: int
    id_addresses: UUID
    products: list[AddProductsSchema]

class ProductSchema(BaseModel):
    id: UUID
    name: str
    description: str
    count: int
    price: float
    discount: float


class ReturningOrdersSchema(BaseModel):
    id: UUID
    address: str
    status: str
    products: list[ProductSchema]
    
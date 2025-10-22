from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import TypeAdapter
from typing import List


class AddressSchema(BaseModel):
    id: UUID = Field(..., alias="id")
    id_user: int = Field(..., alias="id_user")
    country: str = Field(..., alias="country")
    region: str = Field(..., alias="region")
    city: str = Field(..., alias="city")
    street: str = Field(..., alias="street")
    house_number: str = Field(..., alias="house_number")
    quadrature_number: str = Field(..., alias="quadrature_number")
    postal_code: int = Field(..., alias="postal_code")
    created_at: datetime = Field(..., alias="created_at")
    updated_at: datetime = Field(..., alias="updated_at")


adapter = TypeAdapter(List[AddressSchema])
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class AddressSchema():
    id: UUID
    id_user: int
    country: str
    region: str
    city: str
    street: str
    house_number: str
    quadrature_number: str
    postal_code: int
    created_at: datetime
    updated_at: datetime

@dataclass
class CreateAddressSchema():
    id_user: int  | None = None
    country: str  | None = None
    region: str  | None = None
    city: str  | None = None
    street: str  | None = None
    house_number: str  | None = None
    quadrature_number: str  | None = None
    postal_code: int  | None = None
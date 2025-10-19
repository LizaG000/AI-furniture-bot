from dataclasses import dataclass

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
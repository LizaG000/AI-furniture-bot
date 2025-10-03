from dataclasses import dataclass

@dataclass
class CreateUser:
    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone: int | None = None
    email: str | None = None
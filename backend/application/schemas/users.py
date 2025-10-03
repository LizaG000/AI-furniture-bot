from uuid import UUID
from datetime import datetime
from backend.application.schemas.common import BaseModel

class UserSchemas(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: int
    email: str
    created_at: datetime
    updated_at: datetime

class CreateUserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: int
    email: str

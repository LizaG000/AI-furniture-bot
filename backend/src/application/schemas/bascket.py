from src.application.schemas.common import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class CreateBascketSchema(BaseModel):
    id_user: int
    id_product: UUID
    count: int

class BascketSchema(CreateBascketSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

class UpdateBasketSchema(BaseModel):
    count: int

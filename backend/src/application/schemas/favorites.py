from src.application.schemas.common import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class CreateFavoritesSchema(BaseModel):
    id_user: int
    id_product: UUID

class FavoritesSchema(CreateFavoritesSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime


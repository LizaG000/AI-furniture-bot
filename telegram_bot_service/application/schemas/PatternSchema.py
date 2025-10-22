from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import TypeAdapter
from typing import List


class PatternSchema(BaseModel):
    id: UUID = Field(..., alias="id")
    name: str = Field(..., alias="name")
    created_at: datetime = Field(..., alias="created_at")
    updated_at: datetime = Field(..., alias="updated_at")


adapter = TypeAdapter(List[PatternSchema])
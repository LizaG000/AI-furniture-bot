from uuid import UUID
from datetime import datetime
from pydantic import AliasGenerator
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import alias_generators


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(serialization_alias=alias_generators.to_camel),
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

class PatternSchema(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

class CreatePatternSchema(BaseModel):
    name: str


class PatternProductSchema(BaseModel):
    id: UUID
    id_product: UUID
    id_pattern: UUID
    created_at: datetime
    updated_at: datetime

class CreatePatternProductSchema(BaseModel):
    id_product: UUID
    id_pattern: UUID

class CreateColors(BaseModel):
    id_product: UUID
    id_color: UUID

class CreateMaterials(BaseModel):
    id_product: UUID
    id_material: UUID
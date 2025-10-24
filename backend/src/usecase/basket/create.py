from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.bascket import CreateBascketSchema, BascketSchema
from src.infra.postgres.tables import BasketsModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateBasckettUsecase(Usecase[CreateBascketSchema, BascketSchema]):
    session: AsyncSession
    create_bascket: CreateReturningGate[BasketsModel, CreateBascketSchema, BascketSchema]
    async def __call__(self, bascket: CreateBascketSchema) -> BascketSchema:
        async with self.session.begin():
            print(bascket)
            return await self.create_bascket(bascket)

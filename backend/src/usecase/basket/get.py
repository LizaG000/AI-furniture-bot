from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.baskets import GetBasketGate
from src.usecase.basket.schemas import GetBasketSchema
from src.usecase.basket.schemas import ReturnBasketSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetBasketUsecase(Usecase[GetBasketSchema, list[ReturnBasketSchema]]):
    session: AsyncSession
    get_basket_gate: GetBasketGate

    async def __call__(self, data: GetBasketSchema) -> list[ReturnBasketSchema] | list:
        async with self.session.begin():
            products = await self.get_basket_gate(data)
            return products
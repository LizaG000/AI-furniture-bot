from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.orders import GetOrdersAllGate
from src.usecase.orders.schemas import ReturningOrdersSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetOrdersUsecase(Usecase[int, list[ReturningOrdersSchema]]):
    session: AsyncSession
    get_orders: GetOrdersAllGate
    async def __call__(self, id_user: int) -> list[ReturningOrdersSchema]:
        async with self.session.begin():
            return await self.get_orders(id_user=id_user)


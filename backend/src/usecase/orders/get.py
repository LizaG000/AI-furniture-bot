from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.orders import GetOrdersGate
from src.usecase.orders.schemas import ReturnOrderSchema


@dataclass(slots=True, frozen=True, kw_only=True)
class GetAllOrdersUsecase(Usecase[None, list[ReturnOrderSchema]]):
    session: AsyncSession
    get_orders_gate: GetOrdersGate

    async def __call__(self, _: None = None) -> list[ReturnOrderSchema]:
        async with self.session.begin():
            return await self.get_orders_gate()

@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserOrdersUsecase(Usecase[int, list[ReturnOrderSchema]]):
    session: AsyncSession
    get_orders_gate: GetOrdersGate

    async def __call__(self, id_user: int) -> list[ReturnOrderSchema]:
        async with self.session.begin():
            return await self.get_orders_gate(id_user)
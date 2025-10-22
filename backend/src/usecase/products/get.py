from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.products import GetProductsGate
from src.usecase.products.schemas import GetProductsSchema
from src.usecase.products.schemas import ReturnProductsSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetProductUsecase(Usecase[GetProductsSchema, list[ReturnProductsSchema]]):
    session: AsyncSession
    get_products_gate: GetProductsGate

    async def __call__(self, data: GetProductsSchema) -> list[ReturnProductsSchema] | list:
        async with self.session.begin():
            print(1)
            products = await self.get_products_gate(data)
            print(2)
            return products
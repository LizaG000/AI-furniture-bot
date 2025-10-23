from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.favorites import GetFavoritesGate
from src.usecase.favorites.schemas import GetFavoritesSchema
from src.usecase.favorites.schemas import ReturnFavoritesSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class GetFavoritesUsecase(Usecase[GetFavoritesSchema, list[ReturnFavoritesSchema]]):
    session: AsyncSession
    get_favorites_gate: GetFavoritesGate

    async def __call__(self, data: GetFavoritesSchema) -> list[ReturnFavoritesSchema] | list:
        async with self.session.begin():
            products = await self.get_favorites_gate(data)
            return products
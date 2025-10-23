from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.application.schemas.favorites import CreateFavoritesSchema, FavoritesSchema
from src.infra.postgres.tables import FavoritesModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateFavoritesUsecase(Usecase[CreateFavoritesSchema, FavoritesSchema]):
    session: AsyncSession
    create_favorites: CreateReturningGate[FavoritesModel, CreateFavoritesSchema, FavoritesSchema]
    async def __call__(self, favorites: CreateFavoritesSchema) -> FavoritesSchema:
        async with self.session.begin():
            return await self.create_favorites(favorites)

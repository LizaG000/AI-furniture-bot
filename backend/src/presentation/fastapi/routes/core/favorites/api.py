from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.favorites import FavoritesSchema, CreateFavoritesSchema
from src.usecase.favorites.schemas import GetFavoritesSchema, ReturnFavoritesSchema
from src.usecase.favorites.create import CreateFavoritesUsecase
from src.usecase.favorites.get import GetFavoritesUsecase
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.infra.postgres.tables import FavoritesModel
from src.infra.postgres.gateways.base import DeleteGate



ROUTER = APIRouter(route_class=DishkaRoute, tags=["Favorites"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_favorites(
    usecase: FromDishka[CreateFavoritesUsecase],
    data: CreateFavoritesSchema) -> FavoritesSchema:
    return await usecase(data)


@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_favorites(
    usecase: FromDishka[GetFavoritesUsecase],
    data: int) -> list[ReturnFavoritesSchema]:
    return await usecase(GetFavoritesSchema(id_user=data))



@ROUTER.delete('', status_code=status.HTTP_200_OK)
async def delete_favorites(
    session: FromDishka[AsyncSession],
    usecase: FromDishka[DeleteGate[FavoritesModel, UUID]],
    id: UUID) -> None:
    async with session.begin():
        await usecase(id)


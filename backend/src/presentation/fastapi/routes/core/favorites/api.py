from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.favorites import FavoritesSchema, CreateFavoritesSchema
from src.usecase.favorites.create import CreateFavoritesUsecase


ROUTER = APIRouter(route_class=DishkaRoute, tags=["Favorites"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_category(
    usecase: FromDishka[CreateFavoritesUsecase],
    data: CreateFavoritesSchema) -> FavoritesSchema:
    return await usecase(data)
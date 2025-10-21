from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.common import PatternSchema, CreatePatternSchema
from src.infra.postgres.tables import CategoriesModel
from src.infra.postgres.gateways.base import CreateReturningGate, GetAllGate


ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_category(
    session: FromDishka[AsyncSession],
    usecase: FromDishka[CreateReturningGate[CategoriesModel, CreatePatternSchema, PatternSchema]],
    category: CreatePatternSchema) -> PatternSchema:
    async with session.begin():
        return await usecase(category)


@ROUTER.get('', status_code=status.HTTP_200_OK)
async def create_category(
    usecase: FromDishka[GetAllGate[CategoriesModel, PatternSchema]]
    ) -> list[PatternSchema]:
    return await usecase()


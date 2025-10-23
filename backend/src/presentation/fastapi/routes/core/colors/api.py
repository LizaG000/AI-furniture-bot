from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.common import PatternSchema, CreatePatternSchema
from src.infra.postgres.tables import ColorsModel
from src.infra.postgres.gateways.base import CreateReturningGate, GetAllGate

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Colors"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_color(
    session: FromDishka[AsyncSession],
    usecase: FromDishka[CreateReturningGate[ColorsModel, CreatePatternSchema, PatternSchema]],
    color: CreatePatternSchema) -> PatternSchema:
    async with session.begin():
        return await usecase(color)
    

@ROUTER.get('', status_code=status.HTTP_200_OK)
async def create_category(
    usecase: FromDishka[GetAllGate[ColorsModel, PatternSchema]]
    ) -> list[PatternSchema]:
    return await usecase()

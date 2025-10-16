from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.common import PatternSchema, CreatePatternSchema
from src.infra.postgres.tables import ColorsModel
from src.infra.postgres.gateways.base import CreateReturningGate

ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_color(
    usecase: FromDishka[CreateReturningGate[ColorsModel, CreatePatternSchema, PatternSchema]],
    color: CreatePatternSchema) -> PatternSchema:
    return await usecase(color)
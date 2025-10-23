from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from fastapi import status
from src.application.schemas.bascket import BascketSchema, CreateBascketSchema
from src.usecase.bascket.create import CreateBasckettUsecase
from src.infra.postgres.gateways.base import CreateReturningGate, GetAllGate


ROUTER = APIRouter(route_class=DishkaRoute, tags=["Basckets"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_category(
    usecase: FromDishka[CreateBasckettUsecase],
    data: CreateBascketSchema) -> BascketSchema:
    return await usecase(data)
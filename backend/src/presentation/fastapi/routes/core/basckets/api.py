from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from uuid import UUID
from fastapi import status
from src.application.schemas.bascket import BascketSchema, CreateBascketSchema, UpdateBasketSchema
from src.usecase.basket.schemas import GetBasketSchema, ReturnBasketSchema
from src.usecase.basket.create import CreateBasckettUsecase
from src.usecase.basket.get import GetBasketUsecase
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from src.infra.postgres.tables import BasketsModel
from src.infra.postgres.gateways.base import DeleteGate, UpdateReturningGate


ROUTER = APIRouter(route_class=DishkaRoute, tags=["Basckets"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_basket(
    usecase: FromDishka[CreateBasckettUsecase],
    data: CreateBascketSchema) -> BascketSchema:
    return await usecase(data)



@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_basket(
    usecase: FromDishka[GetBasketUsecase],
    data: int) -> list[ReturnBasketSchema]:
    return await usecase(GetBasketSchema(id_user = data))



@ROUTER.delete('', status_code=status.HTTP_200_OK)
async def delete_basket(
    session: FromDishka[AsyncSession],
    usecase: FromDishka[DeleteGate[BasketsModel, UUID]],
    id: UUID) -> None:
    async with session.begin():
        await usecase(id)

@ROUTER.put('', status_code=status.HTTP_200_OK)
async def update_basket(
    session: FromDishka[AsyncSession],
    usecase: FromDishka[UpdateReturningGate[BasketsModel, UpdateBasketSchema, UUID, BascketSchema]],
    id: UUID,
    count: int) -> BascketSchema:
    async with session.begin():
        return await usecase(id, UpdateBasketSchema(count=count))
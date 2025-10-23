from uuid import UUID
from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from src.usecase.orders.get import GetUserOrdersUsecase, GetAllOrdersUsecase
from src.usecase.orders.schemas import ReturnOrderSchema

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Orders"])

@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=list[ReturnOrderSchema])
async def get_all_orders(
    usecase: FromDishka[GetAllOrdersUsecase]) -> list[ReturnOrderSchema]:
    return await usecase()

@ROUTER.get('/user/{user_id}', status_code=status.HTTP_200_OK, response_model=list[ReturnOrderSchema])
async def get_user_orders(
    user_id: int,
    usecase: FromDishka[GetUserOrdersUsecase]) -> list[ReturnOrderSchema]:
    return await usecase(user_id)

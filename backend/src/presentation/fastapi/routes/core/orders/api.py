from fastapi import APIRouter, Query
from fastapi import status
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from src.usecase.orders.schemas import ReturningOrdersSchema, AddOrdersProductsSchema
from src.usecase.orders.create import CreateOrderUsecase
from src.usecase.orders.get import GetOrdersUsecase


ROUTER = APIRouter(route_class=DishkaRoute, tags=["Orders"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_orders(
    usecase: FromDishka[CreateOrderUsecase],
    data: AddOrdersProductsSchema
) -> ReturningOrdersSchema:
    return await usecase(data=data)


@ROUTER.get('', status_code=status.HTTP_200_OK)
async def get_orders(
    usecase: FromDishka[GetOrdersUsecase],
    id_user: int
) -> list[ReturningOrdersSchema] | list:
    return await usecase(id_user=id_user)
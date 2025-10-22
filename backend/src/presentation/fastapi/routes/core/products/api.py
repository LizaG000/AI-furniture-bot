from fastapi import APIRouter, Query
from fastapi import status
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from src.usecase.products.schemas import CreateProductBatchSchema, GetProductsSchema, ReturnProductsSchema
from src.usecase.products.create import CreateProductUsecase
from src.usecase.products.get import GetProductUsecase

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Products"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_products(
    usecase: FromDishka[CreateProductUsecase],
    data: list[CreateProductBatchSchema]
) -> None:
    await usecase(products=data)


@ROUTER.get('', status_code=status.HTTP_200_OK)
async def create_products(
    usecase: FromDishka[GetProductUsecase],
    data: GetProductsSchema = Query(...)
) -> list[ReturnProductsSchema] | list:
    return await usecase(data=data) 
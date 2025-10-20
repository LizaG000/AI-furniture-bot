from fastapi import APIRouter
from fastapi import status
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from src.usecase.products.schemas import CreateProductBatchSchema
from src.usecase.products.create import CreateProductUsecase

ROUTER = APIRouter(route_class=DishkaRoute, tags=["Products"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_products(
    usecase: FromDishka[CreateProductUsecase],
    data: list[CreateProductBatchSchema]
) -> None:
    await usecase(products=data)

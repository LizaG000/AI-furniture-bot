from fastapi import APIRouter
from fastapi import status
from dishka import FromDishka
from src.usecase.products.schemas import CreateProductBatchSchema
from src.usecase.products.create import CreateProductUsecase

ROUTER = APIRouter( tags=["Products"])

@ROUTER.post('', status_code=status.HTTP_200_OK)
async def create_products_batch(
    usecase: FromDishka[CreateProductUsecase],
    data: list[CreateProductBatchSchema]
) -> None:
    await usecase(products=data)

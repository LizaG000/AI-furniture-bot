from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status
from backend.application.schemas.users import CreateUserSchema

ROUTER = APIRouter(route_class=DishkaRoute)

# @ROUTER.post('', status_code=status.HTTP_200_OK)
# async def create_users(
#     # usecase: FromDishka[CreateUserUsecase],
#     user: CreateUserSchema) -> None:
#     pass
#     # await usecase(user)

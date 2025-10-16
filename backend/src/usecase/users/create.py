from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateGate
from src.application.schemas.users import CreateUserSchema
from src.infra.postgres.tables import UsersModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    session: AsyncSession
    create_user: CreateGate[UsersModel, CreateUserSchema]
    async def __call__(self, user: CreateUserSchema) -> None:
        async with self.session.begin():
            await self.create_user(user)

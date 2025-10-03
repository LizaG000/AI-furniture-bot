from sqlalchemy.ext.asyncio import AsyncSession
from backend.usecase.base import Usecase
from backend.infra.postgres.gateways.base import CreateGate
from backend.application.schemas.users import CreateUserSchema
from backend.infra.postgres.tables import UsersModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserUsecase(Usecase[CreateUserSchema, None]):
    session: AsyncSession
    create_user: CreateGate[UsersModel, CreateUserSchema]
    async def __call__(self, user: CreateUserSchema) -> None:
        async with self.session.begin():
            await self.create_user(user)

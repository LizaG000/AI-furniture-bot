# from sqlalchemy.ext.asyncio import AsyncSession
# from backend.usecase.base import Usecase
# from backend.infra.postgres.gateways.base import CreateGate
# from backend.application.schemas.users import CreateUserSchem
# from backend.infra.postgres.tables import UserModel
# from dataclasses import dataclass

# @dataclass(slots=True, frozen=True, kw_only=True)
# class CreateUserUsecase(Usecase[None, None]):
#     session: AsyncSession
    
#     async def __call__(self, ) -> None:
#         pass

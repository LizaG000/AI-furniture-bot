from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.users.api import ROUTER as USER_ROUTER
from src.presentation.fastapi.routes.core.users.api import ROUTER as ADDRESSES_ROUTER
from src.presentation.fastapi.routes.core.categories.api import ROUTER as CATEGORIES_ROUTER
from src.presentation.fastapi.routes.core.materials.api import ROUTER as MATERIALS_ROUTER
from src.presentation.fastapi.routes.core.colors.api import ROUTER as COLORS_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/user', router=USER_ROUTER)
    router.include_router(prefix='/user', router=ADDRESSES_ROUTER)
    router.include_router(prefix='/categories', router=CATEGORIES_ROUTER)
    router.include_router(prefix='/materials', router=MATERIALS_ROUTER)
    router.include_router(prefix='/colors', router=COLORS_ROUTER)
    return router

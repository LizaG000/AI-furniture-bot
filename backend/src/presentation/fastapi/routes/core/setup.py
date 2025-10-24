from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.users.api import ROUTER as USER_ROUTER
from src.presentation.fastapi.routes.core.addresses.api import ROUTER as ADDRESSES_ROUTER
from src.presentation.fastapi.routes.core.categories.api import ROUTER as CATEGORIES_ROUTER
from src.presentation.fastapi.routes.core.materials.api import ROUTER as MATERIALS_ROUTER
from src.presentation.fastapi.routes.core.colors.api import ROUTER as COLORS_ROUTER
from src.presentation.fastapi.routes.core.products.api import ROUTER as PRODUCTS_ROUTER
from src.presentation.fastapi.routes.core.basckets.api import ROUTER as BASCKETS_ROUTER
from src.presentation.fastapi.routes.core.favorites.api import ROUTER as FAVORITES_ROUTER
from src.presentation.fastapi.routes.core.orders.api import ROUTER as ORDERS_ROUTER


def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/user', router=USER_ROUTER)
    router.include_router(prefix='/address', router=ADDRESSES_ROUTER)
    router.include_router(prefix='/categories', router=CATEGORIES_ROUTER)
    router.include_router(prefix='/materials', router=MATERIALS_ROUTER)
    router.include_router(prefix='/colors', router=COLORS_ROUTER)
    router.include_router(prefix='/products', router=PRODUCTS_ROUTER)
    router.include_router(prefix='/basckets', router=BASCKETS_ROUTER)
    router.include_router(prefix='/favorites', router=FAVORITES_ROUTER)
    router.include_router(prefix='/orders', router=ORDERS_ROUTER)

    return router

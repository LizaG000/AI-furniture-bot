from dataclasses import dataclass
from typing import List
from sqlalchemy import select, func, desc
from loguru import logger

from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import (
    BasketsModel,
    ProductsModel,
    CategoriesModel,
    ColorsModel,
    MaterialsModel,
    ProductsColorsModel,
    ProductsMaterialsModel,
)
from src.usecase.basket.schemas import GetBasketSchema, ReturnBasketSchema


@dataclass(slots=True, kw_only=True)
class GetBasketGate(PostgresGateway):
    async def __call__(self, data: GetBasketSchema) -> List[ReturnBasketSchema]:
        """
        Получает все товары из корзины по id_user.
        """
        stmt = (
            select(
                BasketsModel.id,
                BasketsModel.id_user,
                ProductsModel.id.label("id_product"),
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.price,
                BasketsModel.count,
                ProductsModel.count.label("product_count"),
                ProductsModel.discount,
                ProductsModel.length,
                ProductsModel.height,
                ProductsModel.width,
                CategoriesModel.name.label("category"),
                func.coalesce(func.array_agg(func.distinct(ColorsModel.name)), []).label("colors"),
                func.coalesce(func.array_agg(func.distinct(MaterialsModel.name)), []).label("materials"),
                ProductsModel.images,
            )
            .join(ProductsModel, ProductsModel.id == BasketsModel.id_product)
            .join(CategoriesModel, CategoriesModel.id == ProductsModel.id_category)
            .join(ProductsColorsModel, ProductsColorsModel.id_product == ProductsModel.id)
            .join(ColorsModel, ColorsModel.id == ProductsColorsModel.id_color)
            .join(ProductsMaterialsModel, ProductsMaterialsModel.id_product == ProductsModel.id)
            .join(MaterialsModel, MaterialsModel.id == ProductsMaterialsModel.id_material)
            .where(BasketsModel.id_user == data.id_user)
            .group_by(
                BasketsModel.id,
                BasketsModel.id_user,
                ProductsModel.id,
                CategoriesModel.name,
            )
            .order_by(desc(BasketsModel.created_at))
        )

        results = (await self.session.execute(stmt)).mappings().all()
        logger.debug(f"Basket results for user {data.id_user}: {results}")

        if not results:
            return []

        return [ReturnBasketSchema.model_validate(row) for row in results]

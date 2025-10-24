from dataclasses import dataclass
from typing import List
from sqlalchemy import select, func, desc
from loguru import logger

from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import (
    FavoritesModel,
    ProductsModel,
    CategoriesModel,
    ColorsModel,
    MaterialsModel,
    ProductsColorsModel,
    ProductsMaterialsModel,
)
from src.usecase.favorites.schemas import GetFavoritesSchema, ReturnFavoritesSchema


@dataclass(slots=True, kw_only=True)
class GetFavoritesGate(PostgresGateway):
    async def __call__(self, data: GetFavoritesSchema) -> List[ReturnFavoritesSchema]:
        """
        Получает все товары из корзины по id_user.
        """
        stmt = (
            select(
                FavoritesModel.id,
                FavoritesModel.id_user,
                ProductsModel.id.label("id_product"),
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.price,
                ProductsModel.count,
                ProductsModel.discount,
                ProductsModel.length,
                ProductsModel.height,
                ProductsModel.width,
                CategoriesModel.name.label("category"),
                func.coalesce(func.array_agg(func.distinct(ColorsModel.name)), []).label("colors"),
                func.coalesce(func.array_agg(func.distinct(MaterialsModel.name)), []).label("materials"),
                ProductsModel.images,
            )
            .join(ProductsModel, ProductsModel.id == FavoritesModel.id_product)
            .join(CategoriesModel, CategoriesModel.id == ProductsModel.id_category)
            .join(ProductsColorsModel, ProductsColorsModel.id_product == ProductsModel.id)
            .join(ColorsModel, ColorsModel.id == ProductsColorsModel.id_color)
            .join(ProductsMaterialsModel, ProductsMaterialsModel.id_product == ProductsModel.id)
            .join(MaterialsModel, MaterialsModel.id == ProductsMaterialsModel.id_material)
            .where(FavoritesModel.id_user == data.id_user)
            .group_by(
                FavoritesModel.id,
                FavoritesModel.id_user,
                ProductsModel.id,
                CategoriesModel.name,
            )
            .order_by(desc(FavoritesModel.created_at))
        )

        results = (await self.session.execute(stmt)).mappings().all()
        logger.debug(f"Favorites results for user {data.id_user}: {results}")

        if not results:
            return []

        return [ReturnFavoritesSchema.model_validate(row) for row in results]

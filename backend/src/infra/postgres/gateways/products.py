from dataclasses import dataclass
from typing import List
from sqlalchemy import select, func, desc
from sqlalchemy.dialects.postgresql import array_agg
from src.infra.postgres.tables import ProductsModel, ColorsModel, MaterialsModel, CategoriesModel, ProductsColorsModel, ProductsMaterialsModel
from loguru import logger
from src.infra.postgres.gateways.base import PostgresGateway
from src.usecase.products.schemas import GetProductsSchema, ReturnProductsSchema
from sqlalchemy.sql import and_




@dataclass(slots=True, kw_only=True)
class GetProductsGate(PostgresGateway):
    async def __call__(self, data: GetProductsSchema) -> List[ReturnProductsSchema]:
        stmt = (
            select(
                ProductsModel.id,
                ProductsModel.name,
                ProductsModel.description,
                ProductsModel.price,
                ProductsModel.count,
                ProductsModel.discount,
                ProductsModel.length,
                ProductsModel.height,
                ProductsModel.width,
                ProductsModel.images,
                CategoriesModel.name.label("category"),
                func.coalesce(func.array_agg(func.distinct(ColorsModel.name)), []).label("colors"),
                func.coalesce(func.array_agg(func.distinct(MaterialsModel.name)), []).label("materials"),
                ProductsModel.created_at,
                ProductsModel.updated_at,
            )
            .join(CategoriesModel, CategoriesModel.id == ProductsModel.id_category)
            .join(ProductsColorsModel, ProductsColorsModel.id_product == ProductsModel.id)
            .join(ColorsModel, ColorsModel.id == ProductsColorsModel.id_color)
            .join(ProductsMaterialsModel, ProductsMaterialsModel.id_product == ProductsModel.id)
            .join(MaterialsModel, MaterialsModel.id == ProductsMaterialsModel.id_material)
        )

        filters = []
        if  not (data.categories == []):
            filters.append(CategoriesModel.name.in_(data.categories))
        if not (data.colors == []):
            filters.append(ColorsModel.name.in_(data.colors))
        if not (data.materials == []):
            filters.append(MaterialsModel.name.in_(data.materials))

        if not (filters == []):
            stmt = stmt.where(and_(*filters))

        stmt = stmt.group_by(ProductsModel.id, CategoriesModel.name).order_by(desc(ProductsModel.created_at))

        results = (await self.session.execute(stmt)).mappings().all()
        print(results)
        if results == []:
            return []
        return [ReturnProductsSchema.model_validate(row) for row in results]





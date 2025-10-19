from typing import List
from fastapi import APIRouter, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.application.schemas.product import ProductBatchCreateSchema, ProductCreateSchema
from src.infra.postgres.tables import ProductsModel, ColorsModel, MaterialsModel, ProductsColorsModel, ProductsMaterialsModel
from src.infra.postgres.gateways.base import CreateReturningGate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ROUTER = APIRouter(route_class=DishkaRoute, prefix='/products', tags=['Products'])

@ROUTER.post('/batch', status_code=status.HTTP_200_OK)
async def create_products_batch(
    session: FromDishka[AsyncSession],
    products: ProductBatchCreateSchema,
):
    created_products = []

    for p in products.products:
        product = ProductsModel(
            name=p.name,
            description=p.description,
            price=p.price,
            count=p.count,
            discount=p.discount,
            length=p.length,
            height=p.height,
            width=p.width,
            id_category=p.id_category,
            images=p.images,
        )
        #переделать в юзкез создания
        session.add(product)
        await session.flush()  

        for color_name in p.colors:
            color = await session.scalar(select(ColorsModel).where(ColorsModel.name == color_name))
            if color:
                session.add(ProductsColorsModel(id_product=product.id, id_color=color.id))

        for material_name in p.materials:
            material = await session.scalar(select(MaterialsModel).where(MaterialsModel.name == material_name))
            if material:
                session.add(ProductsMaterialsModel(id_product=product.id, id_material=material.id))

        created_products.append(product)

    await session.commit()
    return {"created_count": len(created_products)}

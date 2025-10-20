from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.postgres.tables import (
    ProductsModel,
    ProductsColorsModel,
    ProductsMaterialsModel,
    ColorsModel,
    MaterialsModel
)

async def create_products(session: AsyncSession, products_data: list[dict]):
    created_products = []

    for p in products_data:
        # 1. Создаём продукт
        product = ProductsModel(
            name=p['name'],
            description=p['description'],
            price=p['price'],
            count=p['count'],
            discount=p['discount'],
            length=p['length'],
            height=p['height'],
            width=p['width'],
            id_category=p['id_category'],
            images=p.get('photos', [])
        )
        session.add(product)
        await session.flush()  # получаем product.id

        # 2. Цвета (по названию)
        for color_name in p.get('colors', []):
            color = await session.scalar(select(ColorsModel).where(ColorsModel.name == color_name))
            if color:
                session.add(ProductsColorsModel(product_id=product.id, id_color=color.id))

        # 3. Материалы (по названию)
        for material_name in p.get('materials', []):
            material = await session.scalar(select(MaterialsModel).where(MaterialsModel.name == material_name))
            if material:
                session.add(ProductsMaterialsModel(id_product=product.id, id_material=material.id))

        created_products.append(product)

    await session.commit()
    return created_products

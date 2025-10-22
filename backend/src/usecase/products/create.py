from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate, GetAllGate, CreateGate
from src.application.schemas.product import CreateProductSchema, ProductSchema
from src.application.schemas.common import PatternSchema, CreatePatternSchema, GetColors, GetMaterials, CreateColors, CreateMaterials
from src.usecase.products.schemas import CreateProductBatchSchema
from src.infra.postgres.tables import ProductsModel, ColorsModel, MaterialsModel, CategoriesModel, ProductsColorsModel, ProductsMaterialsModel
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateProductUsecase(Usecase[list[CreateProductBatchSchema], None]):
    session: AsyncSession
    create_product: CreateReturningGate[ProductsModel, CreateProductSchema, ProductSchema]
    get_colors: GetAllGate[ColorsModel, PatternSchema]
    create_color: CreateReturningGate[ColorsModel, CreatePatternSchema, PatternSchema]
    get_materials: GetAllGate[ColorsModel, PatternSchema]
    create_material: CreateReturningGate[MaterialsModel, CreatePatternSchema, PatternSchema]
    get_categories: GetAllGate[CategoriesModel, PatternSchema]
    create_category: CreateReturningGate[CategoriesModel, CreatePatternSchema, PatternSchema]
    create_color_product: CreateReturningGate[ProductsColorsModel, CreateColors, GetColors]
    create_material_product: CreateReturningGate[ProductsMaterialsModel, CreateMaterials, GetMaterials]

    

    async def __call__(self, products: list[CreateProductBatchSchema]) -> None:
        async with self.session.begin():
            # фором по массиву продуктам
            colors = await self.get_colors()
            color_names = []
            materials = await self.get_materials()
            material_names = []
            categories = await self.get_categories()
            category_names = []
            for color in colors:
                color_names.append(color.name)
            for material in materials:
                material_names.append(material.name)
            for category in categories:
                category_names.append(category.name)

            for product in products:  
            #категорию так жеб но без фора
                if product.category_name not in category_names:
                    category = await self.create_category(CreatePatternSchema(name = product.category_name))
                    id_category = category.id
                else:
                    id_category = categories[category_names.index(product.name)].id
            #создаешь продукт

                new_product = await self.create_product(
                    CreateProductSchema(
                        name = product.name,
                        description = product.description,
                        price = product.price,
                        count = product.count,
                        discount = product.discount,
                        length = product.length,
                        height = product.height,
                        width = product.width,
                        id_category = id_category,
                        images = product.images,
                    )
                )

                #фором по цветам проверяя если цвета нет то ты его создаешь используй схему из коммон паттерн крейте схема и паттерн схема для получения цвета

                for color_name in product.colors:
                    if color_name not in color_names:
                        color = await self.create_color(CreatePatternSchema(name = color_name))
                        colors.append(color)
                        color_names.append(color.name)
                        id_color = color.id
                    else:
                        id_color = colors[color_names.index(color_name)].id
                    await self.create_color_product(
                        CreateColors(
                            id_product = new_product.id,
                            id_color = id_color
                        )
                    )


            #то же для материалов
                for material_name in product.materials:
                    if material_name not in material_names:
                        material = await self.create_material(CreatePatternSchema(name = material_name))
                        materials.append(material)
                        material_names.append(material.name)
                        id_material = material.id
                    else: 
                        id_material = materials[material_names.index(material_name)].id
                    await self.create_material_product(
                        CreateMaterials(
                            id_product = new_product.id,
                            id_material = id_material,
                        )
                    )

            #проходишься фором по цветам и добавляешь в таблицу зависимости схема в коммон продукт паттерн схема

            #то же с материалами

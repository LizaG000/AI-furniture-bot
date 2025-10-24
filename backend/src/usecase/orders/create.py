from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from uuid import UUID
from src.infra.postgres.gateways.base import CreateReturningGate, CreateGate, UpdateGate, GetByIdGate
from src.infra.postgres.gateways.orders import GetOrderGate
from src.application.schemas.product import UpdateProductSchema, ProductSchema
from src.application.schemas.orders import CreateOrdersSchema, OrdersSchema, CreateOrdersProductsSchemas
from src.infra.postgres.tables import OrdersModel, OrdersProductsModel, ProductsModel
from src.usecase.orders.schemas import AddOrdersProductsSchema, ReturningOrdersSchema
from dataclasses import dataclass

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateOrderUsecase(Usecase[AddOrdersProductsSchema, ReturningOrdersSchema]):
    session: AsyncSession
    create_order: CreateReturningGate[OrdersModel, CreateOrdersSchema, OrdersSchema]
    create_order_product: CreateGate[OrdersProductsModel, CreateOrdersProductsSchemas]
    get_product: GetByIdGate[ProductsModel, UUID, ProductSchema]
    update_product: UpdateGate[ProductsModel, UpdateProductSchema, UUID]
    get_order: GetOrderGate
    async def __call__(self, data: AddOrdersProductsSchema) -> ReturningOrdersSchema:
        async with self.session.begin():
            # Создать заказ
            order = await self.create_order(CreateOrdersSchema(
                id_user=data.id_user,
                id_addresses=data.id_addresses,
                status="Оформлен",
            ))
            # создать зависимость заказов и продуктов
            for product in data.products:
                await self.create_order_product(
                    CreateOrdersProductsSchemas(
                        id_order=order.id,
                        id_product=product.id_product,
                        count=product.count,
                        price=product.price,
                        discount=product.count
                    )
                )
                product_data = await self.get_product(product.id_product)
                await self.update_product(
                    UpdateProductSchema(
                        count=product_data.count-product.count
                    ),
                    product.id_product
                )
            return await self.get_order(order.id)

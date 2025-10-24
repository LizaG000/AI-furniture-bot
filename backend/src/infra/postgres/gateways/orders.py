from dataclasses import dataclass
from uuid import UUID
import json
from sqlalchemy import select, func, literal
from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import OrdersModel, OrdersProductsModel, ProductsModel, AddressesModel
from src.usecase.orders.schemas import ReturningOrdersSchema
from src.application.errors import NotFoundError

from loguru import logger


@dataclass(slots=True, kw_only=True)
class GetOrderGate(PostgresGateway):

    async def __call__(self, id_order: UUID) -> ReturningOrdersSchema | None:
        stmt = (
            select(
                OrdersModel.id,
                OrdersModel.status,
                func.concat(
                    AddressesModel.country, literal(', '),
                    AddressesModel.region, literal(', '),
                    AddressesModel.city, literal(', '),
                    AddressesModel.street, literal(', '),
                    AddressesModel.house_number, literal(', '),
                    AddressesModel.quadrature_number, literal(', '),
                    AddressesModel.postal_code
                ).label('address'),
                func.json_agg(
                    func.json_build_object(
                        'id', ProductsModel.id,
                        'name', ProductsModel.name,
                        'description', ProductsModel.description,
                        'count', OrdersProductsModel.count,
                        'price', OrdersProductsModel.price,
                        'discount', ProductsModel.discount
                    )
                ).label('products')
            )
            .join(AddressesModel, AddressesModel.id == OrdersModel.id_addresses)
            .join(OrdersProductsModel, OrdersProductsModel.id_order == OrdersModel.id)
            .join(ProductsModel, ProductsModel.id == OrdersProductsModel.id_product)
            .where(OrdersModel.id == id_order)
            .group_by(
                OrdersModel.id,
                OrdersModel.status,
                AddressesModel.country,
                AddressesModel.region,
                AddressesModel.city,
                AddressesModel.street,
                AddressesModel.house_number,
                AddressesModel.quadrature_number,
                AddressesModel.postal_code,
            )
        )

        result = (await self.session.execute(stmt)).mappings().fetchone()
        if result is None:
            raise NotFoundError(OrdersModel)
        
        return ReturningOrdersSchema.model_validate(result)


@dataclass(slots=True, kw_only=True)
class GetOrdersAllGate(PostgresGateway):

    async def __call__(self, id_user: int) -> list[ReturningOrdersSchema] | None:
        stmt = (
            select(
                OrdersModel.id,
                OrdersModel.status,
                func.concat(
                        AddressesModel.country, literal(', '),
                        AddressesModel.region, literal(', '),
                        AddressesModel.city, literal(', '),
                        AddressesModel.street, literal(', '),
                        AddressesModel.house_number, literal(', '),
                        AddressesModel.quadrature_number, literal(', '),
                        AddressesModel.postal_code
                    ).label('address'),
                func.json_agg(
                    func.json_build_object(
                        'id', ProductsModel.id,
                        'name', ProductsModel.name,
                        'description', ProductsModel.description,
                        'count', OrdersProductsModel.count,
                        'price', OrdersProductsModel.price,
                        'discount', ProductsModel.discount
                    )
                ).label('products')
                )
            .join(AddressesModel, AddressesModel.id == OrdersModel.id_addresses)
            .join(OrdersProductsModel, OrdersProductsModel.id_order == OrdersModel.id)
            .join(ProductsModel, ProductsModel.id == OrdersProductsModel.id_product)
            .where(OrdersModel.id_user == id_user)
            .group_by(
                OrdersModel.id,
                OrdersModel.status,
                AddressesModel.country,
                AddressesModel.region,
                AddressesModel.city,
                AddressesModel.street,
                AddressesModel.house_number,
                AddressesModel.quadrature_number,
                AddressesModel.postal_code,
            )
        )

        results = (await self.session.execute(stmt)).mappings().all()
        if results == []:
            return []
        return [ReturningOrdersSchema.model_validate(result) for result in results]
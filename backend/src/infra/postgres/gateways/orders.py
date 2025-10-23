from dataclasses import dataclass
from typing import List, Optional
from sqlalchemy import select, func
from loguru import logger

from src.infra.postgres.gateways.base import PostgresGateway
from src.infra.postgres.tables import OrdersModel, OrdersProductsModel, ProductsModel, AddressesModel, UsersModel

from src.usecase.orders.schemas import ReturnOrderSchema


@dataclass(slots=True, kw_only=True)
class GetOrdersGate(PostgresGateway):
    async def __call__(self, id_user: Optional[int] = None) -> List[ReturnOrderSchema]:

        stmt = (
            select(
                OrdersModel.id.label("order_id"),
                OrdersModel.created_at.label("created_at"),
                func.concat_ws(
                    ", ",
                    AddressesModel.city,
                    AddressesModel.street,
                    AddressesModel.house_number
                ).label("address"),
                func.concat_ws(' ', UsersModel.first_name, UsersModel.last_name).label("user_full_name"),
                func.json_agg(
                    func.json_build_object(
                        "id", ProductsModel.id,
                        "name", ProductsModel.name,
                        "count", OrdersProductsModel.count,
                        "price", OrdersProductsModel.price,
                        "discount", OrdersProductsModel.discount
                    )
                ).label("products"),
                func.sum(
                    (OrdersProductsModel.price - OrdersProductsModel.price * (OrdersProductsModel.discount / 100.0))
                    * OrdersProductsModel.count
                ).label("total_price"),
            )
            .join(AddressesModel, AddressesModel.id == OrdersModel.id_addresses, isouter=True)
            .join(UsersModel, UsersModel.id == OrdersModel.id_user, isouter=True)
            .join(OrdersProductsModel, OrdersProductsModel.id_order == OrdersModel.id)
            .join(ProductsModel, ProductsModel.id == OrdersProductsModel.id_product)
            .group_by(
                OrdersModel.id,
                OrdersModel.created_at,
                AddressesModel.city,
                AddressesModel.street,
                AddressesModel.house_number,
                UsersModel.first_name,
                UsersModel.last_name
            )
            .order_by(OrdersModel.created_at.desc())
        )

        if id_user:
            stmt = stmt.where(OrdersModel.id_user == id_user)

        result = (await self.session.execute(stmt)).mappings().all()

        if not result:
            logger.info("Нет заказов.")
            return []

        return [ReturnOrderSchema.model_validate(row) for row in result]

import uuid
from datetime import datetime
from sqlalchemy import UUID
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ARRAY
from sqlalchemy import Float, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Annotated

uuid_pk = Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )]

created_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]
updated_at = Annotated[datetime, mapped_column(
    DateTime(timezone=True),
    default=func.now(), 
    nullable=False,

)]

class BaseDBModel(DeclarativeBase):
    __tablename__: str
    __table_args__: dict[str, str] | tuple = {'schema': 'db_schema'}

    @classmethod
    def group_by_fields(cls, exclude: list[str] | None = None) -> list:
        payload = []
        if not exclude:
            exclude = []

        for column in cls.__table__.columns:
            if column.key in exclude:
                continue

            payload.append(column)

        return payload

class UsersModel(BaseDBModel):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default='Гость'
    )
    last_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default='Гость'
    )
    middle_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        default=None
    )
    phone: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class CategoriesModel(BaseDBModel):
    __tablename__ = "categories"
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class ColorsModel(BaseDBModel):
    __tablename__ = "colors"
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class MaterialsModel(BaseDBModel):
    __tablename__ = "materials"
    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class ProductsModel(BaseDBModel):
    __tablename__ = 'products'
    id: Mapped[uuid_pk]
    id_category: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.categories.id'),
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    discount: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    length: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    height: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    width: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    images: Mapped[list[str]] = mapped_column(
        ARRAY(String(255)),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class ProductsMaterialsModel(BaseDBModel):
    __tablename__ = 'products_materials'
    id: Mapped[uuid_pk]
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.products.id'),
        nullable=False
    )
    id_material: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.materials.id'),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class ProductsColorsModel(BaseDBModel):
    __tablename__ = 'colors_material'
    id: Mapped[uuid_pk]
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.products.id'),
        nullable=False
    )
    id_color: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.colors.id'),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class BasketsModel(BaseDBModel):
    __tablename__ = 'baskets'
    id: Mapped[uuid_pk]
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.products.id'),
        nullable=False
    )
    count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class AddressesModel(BaseDBModel):
    __tablename__ = 'addresses'
    id: Mapped[uuid_pk]
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    country: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    region: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    city: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    street: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    house_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    quadrature_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    postal_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class OrdersModel(BaseDBModel):
    __tablename__ = 'orders'
    id: Mapped[uuid_pk]
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    id_addresses: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.addresses.id'),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class OrdersProductsModel(BaseDBModel):
    __tablename__ = 'orders_products'
    id: Mapped[uuid_pk]
    id_order: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.orders.id'),
        nullable=False
    )
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.products.id'),
        nullable=False
    )
    count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )
    discount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

class FavoritesModel(BaseDBModel):
    __tablename__ = 'favorites'
    id: Mapped[uuid_pk]
    id_user: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('db_schema.users.id'),
        nullable=False
    )
    id_product: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey('db_schema.products.id'),
        nullable=False
    )
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


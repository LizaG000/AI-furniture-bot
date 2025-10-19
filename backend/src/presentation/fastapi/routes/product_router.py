from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.schemas.product_schema import ProductBatchCreateSchema
from src.usecase.products.create_products import create_products
from src.infra.postgres.provider import PostgresProvider

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/batch")
async def create_products_batch(
    data: ProductBatchCreateSchema,
    session: AsyncSession = Depends(PostgresProvider._get_session_maker)
):
    created = await create_products(session, [p.dict() for p in data.products])
    return {"created_count": len(created)}

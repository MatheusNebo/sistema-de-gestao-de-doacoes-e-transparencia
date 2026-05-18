from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class ProductRepository:

    async def create(self, db: AsyncSession, data):
        product = Product(**data.model_dump())
        db.add(product)
        await db.flush()
        await db.refresh(product)
        return product

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, product_id: int):
        result = await db.execute(
            select(Product).where(Product.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, product_id: int, data):
        product = await self.get_by_id(db, product_id)

        if not product:
            return None

        for key, value in data.model_dump().items():
            setattr(product, key, value)

        await db.flush()
        await db.refresh(product)
        return product

    async def delete(self, db: AsyncSession, product_id: int):
        product = await self.get_by_id(db, product_id)

        if not product:
            return None

        await db.delete(product)
        await db.flush()
        return product
    
    async def get_by_name_and_unit(self, db: AsyncSession, name: str, unit: str):
        result = await db.execute(
            select(Product).where(
                (Product.name == name) & (Product.unit == unit)
            )
        )
        return result.scalar_one_or_none()
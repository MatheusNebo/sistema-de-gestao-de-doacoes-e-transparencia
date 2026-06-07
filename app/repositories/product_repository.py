from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from sqlalchemy.future import select

class ProductRepository:

    async def create(self, db: AsyncSession, data: dict):
        product = Product(**data)
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
    
    async def get_by_ids(self, db: AsyncSession, ids: list[int]):
    # busca todos os produtos que estão na lista de IDs enviada
        query = select(Product).where(Product.product_id.in_(ids))
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, product_id: int, update_data: dict):
        product = await self.get_by_id(db, product_id)

        if not product:
            return None

        for key, value in update_data.items():
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
from app.repositories.product_repository import ProductRepository
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class ProductService:

    def __init__(self):
        self.repository = ProductRepository()

    async def create_product(self, db: AsyncSession, data):
        data.name = data.name.strip().title()
        data.unit = data.unit.strip().lower()

        existing = await self.repository.get_by_name_and_unit(db, data.name, data.unit)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este produto já está cadastrado com esta unidade.")

        product_data = data.model_dump()
        async with db.begin():
            return await self.repository.create(db, product_data)

    async def list_products(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_product(self, db: AsyncSession, product_id: int):
        return await self.repository.get_by_id(db, product_id)

    async def update_product(self, db: AsyncSession, product_id: int, data):
        if data.name:
            data.name = data.name.strip().title()
        if data.unit:
            data.unit = data.unit.strip().lower()

        update_data = data.model_dump(exclude_unset=True)
        async with db.begin():
            return await self.repository.update(db, product_id, update_data)

    async def delete_product(self, db: AsyncSession, product_id: int):
        async with db.begin():
            return await self.repository.delete(db, product_id)
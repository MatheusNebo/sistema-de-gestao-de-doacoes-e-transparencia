from app.repositories.product_repository import ProductRepository
from app.services.audit_service import AuditService
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

class ProductService:

    def __init__(self):
        self.repository = ProductRepository()
        self.audit_service = AuditService()

    async def create_product(self, db: AsyncSession, data):
        data.name = data.name.strip().title()
        data.unit = data.unit.strip().lower()

        existing = await self.repository.get_by_name_and_unit(db, data.name, data.unit)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este produto já está cadastrado com esta unidade.")

        product_data = data.model_dump()
        
        product = await self.repository.create(db, product_data)
            
        # registra na auditoria
        await self.audit_service.log_create(
            db,
            entity_type="product",
            entity_id=product.product_id,
            new_value=product_data
        )
        await db.commit()
        return product

    async def list_products(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_product(self, db: AsyncSession, product_id: int):
        return await self.repository.get_by_id(db, product_id)

    async def update_product(self, db: AsyncSession, product_id: int, data):
        current_product = await self.repository.get_by_id(db, product_id)
        if not current_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
            
        if data.name:
            data.name = data.name.strip().title()
        if data.unit:
            data.unit = data.unit.strip().lower()

        update_data = data.model_dump(exclude_unset=True)
        
        # guarda valor antigo para auditoria
        old_value = {
            "name": current_product.name,
            "category": current_product.category,
            "unit": current_product.unit,
        }
        
        async with db.begin():
            updated = await self.repository.update(db, product_id, update_data)
            
            # registra na auditoria
            await self.audit_service.log_update(
                db,
                entity_type="product",
                entity_id=product_id,
                old_value=old_value,
                new_value=update_data
            )
            
            return updated

    async def delete_product(self, db: AsyncSession, product_id: int):
        product = await self.repository.get_by_id(db, product_id)
        if not product:
            return None
            
        # guarda dados para auditoria
        old_value = {
            "product_id": product.product_id,
            "name": product.name,
            "category": product.category,
            "unit": product.unit,
        }
        
        async with db.begin():
            await self.repository.delete(db, product_id)
            
            # registra na auditoria
            await self.audit_service.log_delete(
                db,
                entity_type="product",
                entity_id=product_id,
                old_value=old_value
            )
            
            return product
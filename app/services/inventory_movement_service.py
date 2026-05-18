from app.repositories.inventory_movement_repository import InventoryMovementRepository
from sqlalchemy.ext.asyncio import AsyncSession

class InventoryMovementService:
    def __init__(self):
        self.repository = InventoryMovementRepository()

    async def get_history(self, db: AsyncSession, product_id: int = None):
        # retorna o histórico geral ou filtrado por produto
        if product_id:
            return await self.repository.get_by_product(db, product_id)
        return await self.repository.get_all(db)

    async def get_movement_details(self, db: AsyncSession, movement_id: int):
        return await self.repository.get_by_id(db, movement_id)
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.inventory_movement import InventoryMovement
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class InventoryMovementRepository:
    async def create(self, db: AsyncSession, data):
        db_movement = InventoryMovement(
            product_id=data.product_id,
            movement_type=data.movement_type,
            quantity=data.quantity,
            source=data.source
        )
        db.add(db_movement)
        await db.flush()
        await db.refresh(db_movement)
        return db_movement

    async def get_history_by_product(self, db: AsyncSession, product_id: int):
        result = await db.execute(
            select(InventoryMovement).where(
                InventoryMovement.product_id == product_id
            )
        )
        return result.scalars().all()
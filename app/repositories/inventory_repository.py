from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.inventory import Inventory
from sqlalchemy.exc import SQLAlchemyError

class InventoryRepository:

    async def create(self, db: AsyncSession, data):
        if hasattr(data, "model_dump"):
            inventory_data = data.model_dump()
        else:
            inventory_data = data

        inventory = Inventory(**inventory_data)
        db.add(inventory)
        await db.flush()
        await db.refresh(inventory)
        return inventory

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Inventory))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, inventory_id: int):
        result = await db.execute(
            select(Inventory).where(Inventory.inventory_id == inventory_id)
        )
        return result.scalar_one_or_none()
    
    async def update(self, db: AsyncSession, inventory_id: int, data):
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return await self.get_by_id(db, inventory_id)

        inventory = await self.get_by_id(db, inventory_id)
        if not inventory:
            return None
            
        for key, value in update_data.items():
            setattr(inventory, key, value)

        await db.flush()
        return await self.get_by_id(db, inventory_id)

    async def delete(self, db: AsyncSession, inventory_id: int):
        inventory = await self.get_by_id(db, inventory_id)

        if not inventory:
            return None

        await db.delete(inventory)
        await db.flush()
        return inventory

    async def get_by_product_and_batch(self, db: AsyncSession, product_id: int, batch: str):
        result = await db.execute(
            select(Inventory).where(
                (Inventory.product_id == product_id),
                (Inventory.batch == batch)
            ).with_for_update()  # bloqueia o registro para evitar concorrência
        )
        return result.scalar_one_or_none()

    async def get_total_quantity(self, db: AsyncSession, product_id: int):
        result = await db.execute(
            select(func.sum(Inventory.quantity)).where(
                Inventory.product_id == product_id
            )
        )
        total = result.scalar()
        return total or 0

    async def update_quantity(self, db: AsyncSession, inventory_id: int, new_quantity: float):
        inventory = await self.get_by_id(db, inventory_id)
        if not inventory:
            return False
        inventory.quantity = new_quantity
        await db.flush()
        return True

    async def subtract_quantity(self, db: AsyncSession, product_id: int, quantity: float):
        # subtrai quantidade do inventário usando FIFO (primeiro lote a vencer primeiro)
        result = await db.execute(
            select(Inventory).where(
                Inventory.product_id == product_id
            ).order_by(Inventory.expiration_date).with_for_update()  # bloqueia os registros para evitar saidas concorrentes 
        )
        inventories = result.scalars().all()

        if not inventories:
            raise ValueError(f"Nenhum inventário encontrado para produto {product_id}")

        remaining_to_subtract = quantity

        # percorre lotes na ordem FIFO e subtrai
        for inventory in inventories:
            if remaining_to_subtract <= 0:
                break

            if inventory.quantity >= remaining_to_subtract:
                inventory.quantity -= remaining_to_subtract
                remaining_to_subtract = 0
            else:
                remaining_to_subtract -= inventory.quantity
                inventory.quantity = 0

        await db.flush()
        return True

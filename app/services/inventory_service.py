from app.repositories.inventory_repository import InventoryRepository
from app.repositories.inventory_movement_repository import InventoryMovementRepository
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

class InventoryService:

    def __init__(self):
        self.repository = InventoryRepository()
        self.movement_repository = InventoryMovementRepository() 

    async def register_movement(self, db: AsyncSession, movement_data):
        try:
            async with db.begin():
                # registra o movimento (Histórico)
                movement = await self.movement_repository.create(db, movement_data)

                # lógica de Entrada (Entry)
                if movement.movement_type == 'entrada':
                    # busca lote bloqueando para escrita (Pessimistic Locking)
                    existing_stock = await self.repository.get_by_product_and_batch(
                        db, movement.product_id, movement_data.batch
                    )
                    
                    if existing_stock:
                        # soma as quantidades convertendo para Decimal para segurança (padrão json em float pode causar erros)
                        new_qty = Decimal(str(existing_stock.quantity)) + Decimal(str(movement.quantity))
                        await self.repository.update_quantity(db, existing_stock.inventory_id, new_qty)
                    else:
                        # cria novo registro no inventário (novo lote)
                        await self.repository.create(db, movement_data)

                # lógica de Saída ou Perda (Exit/Loss)
                else:
                    total_stock = await self.repository.get_total_quantity(db, movement.product_id)
                    if total_stock < movement.quantity:
                        # se não houver saldo, o erro interrompe a transação
                        raise HTTPException(
                            status_code=400, 
                            detail=f"Saldo insuficiente. Disponível: {total_stock}"
                        )
                    
                    # subtrai usando a lógica FIFO
                    await self.repository.subtract_quantity(db, movement.product_id, movement.quantity)

                return movement

        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Erro crítico de inventário: {str(e)}")

    async def list_inventories(self, db: AsyncSession):
        return await self.repository.get_all(db)
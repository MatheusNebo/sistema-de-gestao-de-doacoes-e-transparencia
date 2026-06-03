from app.repositories.inventory_repository import InventoryRepository
from app.repositories.inventory_movement_repository import InventoryMovementRepository
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from app.enums import MovementType, MovementSource
from app.exceptions import DomainError

class InventoryService:

    def __init__(self):
        self.repository = InventoryRepository()
        self.movement_repository = InventoryMovementRepository() 

    async def register_movement(self, db: AsyncSession, movement_data, batch: str = None, expiration_date = None):
        try:
            movement_dict = movement_data.model_dump()

            # normaliza strings para enums quando fornecidos como texto
            if movement_dict.get("movement_type"):
                movement_dict["movement_type"] = MovementType(movement_dict["movement_type"])
            if movement_dict.get("source"):
                movement_dict["source"] = MovementSource(movement_dict["source"])

            async with db.begin():
                # registra o movimento (Histórico)
                movement = await self.movement_repository.create(db, movement_dict)

                # lógica de entrada (Entry)
                if movement.movement_type == MovementType.ENTRADA:
                    # busca lote bloqueando para escrita 
                    existing_stock = await self.repository.get_by_product_and_batch(
                        db, movement.product_id, batch
                    )

                    if existing_stock:
                        # soma as quantidades convertendo para Decimal para segurança
                        new_qty = Decimal(str(existing_stock.quantity)) + Decimal(str(movement.quantity))
                        await self.repository.update_quantity(db, existing_stock.inventory_id, new_qty)
                    else:
                        # cria novo registro no inventário (novo lote)
                        inventory_data = {
                            "product_id": movement.product_id,
                            "quantity": movement.quantity,
                            "batch": batch,
                            "expiration_date": expiration_date
                        }
                        await self.repository.create(db, inventory_data)

                # lógica de Saída ou Perda (Exit/Loss)
                else:
                    total_stock = await self.repository.get_total_quantity(db, movement.product_id)
                    if total_stock < movement.quantity:
                        # lança erro de domínio para o handler global
                        raise DomainError(f"Saldo insuficiente. Disponível: {total_stock}")

                    # subtrai usando a lógica FIFO
                    await self.repository.subtract_quantity(db, movement.product_id, movement.quantity)

                return movement

        except DomainError:
            raise
        except Exception:
            # erro genérico — o handler global converte em resposta 500 sem expor detalhes
            raise

    async def list_inventories(self, db: AsyncSession):
        return await self.repository.get_all(db)
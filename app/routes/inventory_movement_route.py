from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.inventory_movement_service import InventoryMovementService
from app.services.inventory_service import InventoryService # para o POST
from app.schemas.inventory_movement_schema import InventoryMovementCreate

router = APIRouter(prefix="/movements", tags=["Movements"])
movement_service = InventoryMovementService()
inventory_service = InventoryService()

@router.get("/")
async def list_history(
    product_id: int = Query(None), 
    db: AsyncSession = Depends(get_db)
):
    # retorna o extrato de movimentações (entradas e saídas)
    return await movement_service.get_history(db, product_id)

@router.post("/")
async def create_movement(
    movement_data: InventoryMovementCreate, 
    db: AsyncSession = Depends(get_db)
):
    
    # ponto de entrada para novas movimentações
    # chama o InventoryService porque ele garante que o saldo seja atualizado
    return await inventory_service.register_movement(db, movement_data)
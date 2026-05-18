from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas.inventory_schema import InventoryResponse
from app.schemas.inventory_movement_schema import InventoryMovementCreate, InventoryMovementResponse
from app.services import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/", response_model=List[InventoryResponse])
async def get_current_inventory(db: AsyncSession = Depends(get_db)):    
    return await inventory_service.get_all_inventory(db)

@router.post("/move", response_model=InventoryMovementResponse, status_code=status.HTTP_201_CREATED)
async def create_movement(movement: InventoryMovementCreate, db: AsyncSession = Depends(get_db)):

    # o service deve atualizar a tabela 'inventory' automaticamente após o sucesso.
    return await inventory_service.register_movement(db, movement)

@router.get("/product/{product_id}", response_model=List[InventoryResponse])
async def get_inventory_by_product(product_id: int, db: AsyncSession = Depends(get_db)):
    
    items = await inventory_service.get_by_product(db, product_id)
    if not items:
        raise HTTPException(status_code=404, detail="Produto não encontrado no estoque.")
    return items
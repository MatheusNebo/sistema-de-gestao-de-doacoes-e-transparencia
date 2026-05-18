from pydantic import BaseModel, Field
from datetime import datetime

class InventoryMovementCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: float = Field(..., gt=0) # movimentação não pode ser zero
    movement_type: str = Field(..., pattern="^(entrada|saida|perda)$")
    source: str = Field(..., pattern="^(doacao|distribuicao|ajuste)$")

class InventoryMovementResponse(InventoryMovementCreate):
    inventory_movement_id: int
    movement_date: datetime

    class Config:
        from_attributes = True
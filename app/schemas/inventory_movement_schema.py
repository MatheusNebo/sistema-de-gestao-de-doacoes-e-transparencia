from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal
from typing import Optional

class InventoryMovementCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0) # movimentação nunca pode ser zero
    movement_type: str = Field(..., pattern="^(entrada|saida|perda)$")
    source: str = Field(..., pattern="^(doacao|distribuicao|ajuste)$")
    
    # adicionados para que o Service possa registrar o vínculo histórico
    donor_id: Optional[int] = None
    beneficiary_id: Optional[int] = None
    user_id: Optional[int] = None

class InventoryMovementResponse(InventoryMovementCreate):
    inventory_movement_id: int
    movement_date: datetime

    class Config:
        from_attributes = True
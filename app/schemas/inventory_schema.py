from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal

class InventoryBase(BaseModel):
    # alterado para Decimal para manter consistência com o banco
    quantity: Decimal = Field(..., ge=0, example="10.50")
    batch: str = Field(..., max_length=50, example="Lote A123")
    expiration_date: date = Field(..., example="2026-12-31")

class InventoryCreate(InventoryBase):
    product_id: int = Field(..., gt=0, example=1)
    entry_date: Optional[date] = Field(default_factory=date.today)

class InventoryUpdate(BaseModel):
    quantity: Optional[Decimal] = Field(None, ge=0)
    expiration_date: Optional[date] = None
    entry_date: Optional[date] = None

class InventoryResponse(InventoryBase):
    inventory_id: int
    product_id: int
    entry_date: date

    class Config:
        from_attributes = True
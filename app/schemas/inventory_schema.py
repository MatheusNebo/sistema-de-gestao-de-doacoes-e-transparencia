from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class InventoryBase(BaseModel):
    product_id: int = Field(..., gt=0, example=1)
    quantity: float = Field(..., ge=0, example=10.5)
    batch: Optional[str] = Field(None, max_length=50, example="Lote A123")
    expiration_date: date = Field(..., example="2026-12-31")
    entry_date: date = Field(..., example="2026-01-01")


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    product_id: Optional[int] = Field(None, gt=0)
    quantity: Optional[float] = Field(None, ge=0)

    batch: Optional[str] = Field(None, max_length=50)
    expiration_date: Optional[date] = Field (None, examples="2026-12-31")
    entry_date: Optional[date] = Field(None, example="2026-01-01")


class InventoryResponse(InventoryBase):
    inventory_id: int

    class Config:
        from_attributes = True
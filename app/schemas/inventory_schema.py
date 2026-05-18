from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class InventoryBase(BaseModel):
    # quantidade deve ser obrigatória na base para garantir que nunca seja nula
    quantity: float = Field(..., ge=0, example=10.5)
    batch: str = Field(..., max_length=50, example="Lote A123")
    # mantem obrigatório para segurança
    expiration_date: date = Field(..., example="2026-12-31")

class InventoryCreate(InventoryBase):
    product_id: int = Field(..., gt=0, example=1)
    # entry_date costuma ser gerada pelo banco, mas caso o WordPress envie uma data, aceita. Se não for enviada, usamos a data atual:
    entry_date: Optional[date] = Field(default_factory=date.today)

class InventoryUpdate(BaseModel):
    # no Update, NÃO inclui product_id nem batch por segurança
    # permite atualizar apenas quantidade ou datas de correção
    quantity: Optional[float] = Field(None, ge=0)
    expiration_date: Optional[date] = None
    entry_date: Optional[date] = None

class InventoryResponse(InventoryBase):
    inventory_id: int
    product_id: int
    entry_date: date

    class Config:
        from_attributes = True
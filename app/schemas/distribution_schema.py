from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from app.schemas.distribution_item_schema import DistributionItemCreate, DistributionItemResponse

class DistributionCreate(BaseModel):
    beneficiary_id: int = Field(..., gt=0)
    distribution_date: date
    items: List[DistributionItemCreate] = Field(..., min_length=1) 
    # min_length=1 garante que não exista distribuição vazia
    # utilização de lista para manter consistência com a criação de doações, onde os itens são parte do processo de criação

class DistributionUpdate(BaseModel):
    # apenas cabeçalho sem lista de itens.
    beneficiary_id: Optional[int] = Field(None, gt=0)
    distribution_date: Optional[date] = None

class DistributionResponse(BaseModel):
    distribution_id: int
    beneficiary_id: int
    distribution_date: date
    items: List[DistributionItemResponse] = []

    class Config:
        from_attributes = True
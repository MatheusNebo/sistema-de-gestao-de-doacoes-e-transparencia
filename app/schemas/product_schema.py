from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.enums import UnitType

class ProductBase(BaseModel):
    # o Field evita strings vazias e define limites razoáveis
    name: str = Field(..., min_length=2, max_length=100, example="Arroz Integral")
    category: Optional[str] = Field(None, max_length=50, example="Alimentos Não Perecíveis")
    unit: UnitType = Field(..., example="kg")

    # validação para garantir que a unidade seja sempre armazenada em minúsculas
    @field_validator('unit', mode='before')
    @classmethod
    def to_lower(cls, v: str) -> str:
        return v.lower().strip() if isinstance(v, str) else v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    unit: Optional[UnitType] = Field(None)

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True
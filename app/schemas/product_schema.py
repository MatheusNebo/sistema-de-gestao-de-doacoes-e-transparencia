from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    # O Field evita strings vazias e define limites razoáveis
    name: str = Field(..., min_length=2, max_length=100, example="Arroz Integral")
    category: Optional[str] = Field(None, max_length=50, example="Alimentos Não Perecíveis")
    unit: str = Field(..., min_length=1, max_length=20, example="kg")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    # Aqui todos são Optional e não possuem o "..." (que indica obrigatoriedade)
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = Field(None, max_length=50)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)

class ProductResponse(ProductBase):
    product_id: int

    class Config:
        from_attributes = True
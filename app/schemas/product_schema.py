from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    unit: str

class ProductResponse(ProductCreate):
    product_id: int

    class Config:
        from_attributes = True
from pydantic import BaseModel, Field
from decimal import Decimal

class DistributionItemBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)

class DistributionItemCreate(DistributionItemBase):
    pass

class DistributionItemResponse(DistributionItemBase):
    distribution_item_id: int

    class Config:
        from_attributes = True
from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.enums import DonationType

class DonationItemBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0)

    batch: Optional[str] = Field(None, max_length=50)
    expiration_date: Optional[date] = None

    @field_validator("quantity", mode="before")
    @classmethod
    def normalize_quantity(cls, value):
        if isinstance(value, str):
            return Decimal(value)
        return value


class DonationItemCreate(DonationItemBase):
    pass


class DonationItemResponse(DonationItemBase):
    donation_item_id: int

    class Config:
        from_attributes = True


class DonationBase(BaseModel):
    donor_id: int = Field(..., gt=0)
    donation_date: date
    donation_type: DonationType
    total_value: Optional[Decimal] = Field(None, ge=0)
    items: Optional[List[DonationItemCreate]] = None

    @model_validator(mode="after")
    def validate_donation(self):
        if self.donation_type == DonationType.FOOD and not self.items:
            raise ValueError("Doações do tipo food devem possuir itens")
        if self.donation_type == DonationType.FINANCIAL and self.total_value is None:
            raise ValueError("Doações financeiras exigem total_value")
        return self


class DonationCreate(DonationBase):
    pass

# sem classe update por ser uma tabela de registros históricos, onde não se espera alterações após a criação. Se necessário, 
# pode-se criar uma classe de update que permita apenas a modificação de campos específicos, 
# como a data da doação ou o tipo, mas isso deve ser avaliado com cuidado para não comprometer a integridade dos dados históricos.

    @model_validator(mode="after")
    def validate_donation(self):
        if self.donation_type == DonationType.FOOD and self.items is None:
            return self
        if self.donation_type == DonationType.FOOD and not self.items:
            raise ValueError("Doações do tipo food devem possuir itens")
        return self


class DonationResponse(DonationBase):
    donation_id: int
    items: List[DonationItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

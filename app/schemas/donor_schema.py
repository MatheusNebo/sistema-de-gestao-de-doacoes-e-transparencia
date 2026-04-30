from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from datetime import datetime
from app.enums import DonorType


class DonorBase(BaseModel):
    donor_type: DonorType

    name: Optional[str] = None
    cpf: Optional[str] = None

    company_name: Optional[str] = None
    cnpj: Optional[str] = None

    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class DonorCreate(DonorBase):

    @model_validator(mode="after")
    def validate_pf_pj(self):

        if self.donor_type == DonorType.PF:
            if not self.name or not self.cpf:
                raise ValueError("Pessoa física exige nome e CPF")

            if self.company_name or self.cnpj:
                raise ValueError("Pessoa física não deve possuir razão social ou CNPJ")

        elif self.donor_type == DonorType.PJ:
            if not self.company_name or not self.cnpj:
                raise ValueError("Pessoa jurídica exige razão social e CNPJ")

            if self.name or self.cpf:
                raise ValueError("Pessoa jurídica não deve possuir nome ou CPF")

        return self


class DonorUpdate(BaseModel):
    donor_type: Optional[DonorType] = None

    name: Optional[str] = None
    cpf: Optional[str] = None

    company_name: Optional[str] = None
    cnpj: Optional[str] = None

    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class DonorResponse(DonorBase):
    donor_id: int
    created_at: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime
from app.enums import DonorType


class DonorBase(BaseModel):
    donor_type: DonorType

    name: Optional[str] = Field(None, min_length=2, max_length=150, example="João Silva")
    cpf: Optional[str] = Field(None, min_length=11, max_length=14, example="123.456.789-00")

    company_name: Optional[str] = Field(None, min_length=2, max_length=150, example="Empresa LTDA")
    cnpj: Optional[str] = Field(None, min_length=14, max_length=18, example="12.345.678/0001-99")

    email: Optional[EmailStr] = Field(None, example="email@email.com")
    phone: Optional[str] = Field(None, max_length=20, example="14999999999")


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

    name: Optional[str] = Field(None, min_length=2, max_length=150)
    cpf: Optional[str] = Field(None, min_length=11, max_length=14)

    company_name: Optional[str] = Field(None, min_length=2, max_length=150)
    cnpj: Optional[str] = Field(None, min_length=14, max_length=18)

    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)


class DonorResponse(DonorBase):
    donor_id: int
    created_at: datetime

    class Config:
        from_attributes = True
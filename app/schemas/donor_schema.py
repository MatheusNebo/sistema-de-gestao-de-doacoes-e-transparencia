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

class DonorCreate(BaseModel):
    donor_type: str = Field(..., pattern="^(PF|PJ)$", example="PF")
    name: str = Field(..., min_length=2, example="João Silva")
    
    # todos começam como opcionais para o Pydantic não travar de início
    cpf: Optional[str] = Field(None, min_length=11, max_length=11, example="12345678901")
    company_name: Optional[str] = Field(None, min_length=2, max_length=100, example="ONG Ajuda Mais")
    cnpj: Optional[str] = Field(None, min_length=14, max_length=14, example="12345678000100")

    @model_validator(mode="before")
    @classmethod
    def empty_strings_to_none(cls, data: dict) -> dict:
        
        #interceptor: Se o front-end ou Swagger enviar "", convertemos para None.
        #isso impede que o 'min_length' quebre a validação de campos vazios.
        
        if isinstance(data, dict):
            for key, value in data.items():
                if value == "":
                    data[key] = None
        return data

    @model_validator(mode="after")
    def validate_conditional_fields(self):
        
        # validação de Negócio: Garante os campos certos com base no tipo de doador.
        
        if self.donor_type == "PF" and not self.cpf:
            raise ValueError("O campo 'cpf' é obrigatório para doadores do tipo Pessoa Física (PF).")
        
        if self.donor_type == "PJ":
            if not self.cnpj or not self.company_name:
                raise ValueError("Os campos 'cnpj' e 'company_name' são obrigatórios para Pessoa Jurídica (PJ).")
        
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
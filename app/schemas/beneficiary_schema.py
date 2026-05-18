from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, date

class BeneficiaryBase(BaseModel):
    # base comum para compartilhamento de campos
    name: str = Field(..., min_length=3, max_length=150, example="Maria da Silva")
    address: str = Field(..., min_length=5, example="Rua das Flores, 123")
    
    # mudamos para date pura para evitar problemas de fuso horário
    birth_date: date = Field(..., example="1985-05-15")
    
    # campos que aceitam nulo (Deixados como Optional explicitamente)
    email: Optional[EmailStr] = Field(None, max_length=100, example="maria@email.com")
    city: Optional[str] = Field(None, max_length=100, example="São Paulo")
    telephone: Optional[str] = Field(None, max_length=20, example="11999998888")
    household_size: Optional[int] = Field(None, gt=0, example=4)
    family_income: Optional[float] = Field(None, ge=0, example=1412.00)

class BeneficiaryCreate(BeneficiaryBase):
    # o CPF só é exigido e enviado na CRIAÇÃO do beneficiário
    # max_length=14 permite formatos com pontos e traço: "123.456.789-00"
    cpf: str = Field(..., min_length=11, max_length=14, example="12345678900")

class BeneficiaryUpdate(BaseModel):
    # no Update tudo vira opcional, e o CPF NÃO entra aqui por segurança
    name: Optional[str] = Field(None, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=100)
    birth_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    telephone: Optional[str] = Field(None, max_length=20)
    household_size: Optional[int] = Field(None, gt=0)
    family_income: Optional[float] = Field(None, ge=0)

class BeneficiaryResponse(BeneficiaryBase):
    # retorna os dados base + as informações geradas pelo banco
    beneficiary_id: int
    cpf: str # o CPF é devolvido na resposta para leitura do painel
    created_at: datetime

    class Config:
        from_attributes = True
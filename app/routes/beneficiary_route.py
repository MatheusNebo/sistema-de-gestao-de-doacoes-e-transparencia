from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.beneficiary_schema import BeneficiaryCreate, BeneficiaryUpdate, BeneficiaryResponse
from app.services.beneficiary_service import BeneficiaryService

router = APIRouter(prefix="/beneficiaries", tags=["Beneficiaries"])

service = BeneficiaryService()

@router.post("/", response_model=BeneficiaryResponse)
async def create_beneficiary(data: BeneficiaryCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_beneficiary(db, data)

@router.get("/", response_model=list[BeneficiaryResponse])
async def list_beneficiaries(db: AsyncSession = Depends(get_db)):
    return await service.list_beneficiaries(db)

@router.get("/{beneficiary_id}", response_model=BeneficiaryResponse)
async def get_beneficiary(beneficiary_id: int, db: AsyncSession = Depends(get_db)):
    beneficiary = await service.get_beneficiary(db, beneficiary_id)
    
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiário não encontrado")
    
    return beneficiary

@router.put("/{beneficiary_id}", response_model=BeneficiaryResponse)
async def update_beneficiary(beneficiary_id: int, data: BeneficiaryUpdate, db: AsyncSession = Depends(get_db)):
    beneficiary = await service.update_beneficiary(db, beneficiary_id, data)
    
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiário não encontrado")
    
    return beneficiary

@router.delete("/{beneficiary_id}")
async def delete_beneficiary(beneficiary_id: int, db: AsyncSession = Depends(get_db)):
    beneficiary = await service.delete_beneficiary(db, beneficiary_id)
    
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiário não encontrado")
    
    return {"message": "Beneficiário removido com sucesso"}

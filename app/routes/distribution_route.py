from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.distribution_schema import DistributionCreate, DistributionResponse
from app.services.distribution_service import DistributionService

router = APIRouter(prefix="/distributions", tags=["Distributions"])

service = DistributionService()

@router.post("/", response_model=DistributionResponse)
async def create_distribution(data: DistributionCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_distribution(db, data)

@router.get("/{distribution_id}", response_model=DistributionResponse)
async def get_distribution(distribution_id: int, db: AsyncSession = Depends(get_db)):
    distribution = await service.repository.get_by_id(db, distribution_id)
    
    if not distribution:
        raise HTTPException(status_code=404, detail="Distribuição não encontrada")
    
    return distribution

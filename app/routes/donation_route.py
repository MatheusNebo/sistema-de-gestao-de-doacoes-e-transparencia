from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.donation_schema import DonationCreate, DonationUpdate, DonationResponse
from app.services.donation_service import DonationService

router = APIRouter(prefix="/donations", tags=["Donations"])
service = DonationService()

@router.post("/", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
async def create_donation(data: DonationCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_donation(db, data)

@router.get("/", response_model=list[DonationResponse])
async def list_donations(db: AsyncSession = Depends(get_db)):
    return await service.list_donations(db)

@router.get("/{donation_id}", response_model=DonationResponse)
async def get_donation(donation_id: int, db: AsyncSession = Depends(get_db)):
    return await service.get_donation(db, donation_id)

@router.delete("/{donation_id}")
async def delete_donation(donation_id: int, db: AsyncSession = Depends(get_db)):
    await service.delete_donation(db, donation_id)
    return {"message": "Doação removida com sucesso"}

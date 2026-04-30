from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.donor_schema import DonorCreate, DonorResponse
from app.services.donor_service import DonorService

router = APIRouter(prefix="/donors", tags=["Donors"])

service = DonorService()

@router.post("/", response_model=DonorResponse)
def create_donor(data: DonorCreate, db: Session = Depends(get_db)):
    return service.create_donor(db, data)

@router.get("/", response_model=list[DonorResponse])
def list_donors(db: Session = Depends(get_db)):
    return service.list_donors(db)

@router.get("/{donor_id}", response_model=DonorResponse)
def get_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = service.get_donor(db, donor_id)

    if not donor:
        raise HTTPException(status_code=404, detail="Doador não encontrado")

    return donor

@router.put("/{donor_id}", response_model=DonorResponse)
def update_donor(donor_id: int, data: DonorCreate, db: Session = Depends(get_db)):
    donor = service.update_donor(db, donor_id, data)

    if not donor:
        raise HTTPException(status_code=404, detail="Doador não encontrado")

    return donor

@router.delete("/{donor_id}")
def delete_donor(donor_id: int, db: Session = Depends(get_db)):
    donor = service.delete_donor(db, donor_id)

    if not donor:
        raise HTTPException(status_code=404, detail="Doador não encontrado")

    return {"message": "Doador removido com sucesso"}
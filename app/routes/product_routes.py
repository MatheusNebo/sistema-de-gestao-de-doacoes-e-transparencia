from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

service = ProductService()

@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, data)

@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return service.list_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = service.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = service.update_product(db, product_id, data)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = service.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return {"message": "Produto removido com sucesso"}
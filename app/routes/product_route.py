from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.product_schema import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])

service = ProductService()

@router.post("/", response_model=ProductResponse)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_product(db, data)

@router.get("/", response_model=list[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await service.list_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await service.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, data: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await service.update_product(db, product_id, data)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await service.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return {"message": "Produto removido com sucesso"}
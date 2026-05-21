from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.donation_repository import DonationRepository
from app.repositories.donor_repository import DonorRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.donation_schema import DonationCreate, DonationUpdate
from app.enums import DonationType


class DonationService:

    def __init__(self):
        self.repository = DonationRepository()
        self.donor_repository = DonorRepository()
        self.product_repository = ProductRepository()

    async def create_donation(self, db: AsyncSession, data: DonationCreate):
        donor = await self.donor_repository.get_by_id(db, data.donor_id)
        if not donor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doador não encontrado")

        donation_data = data.model_dump()
        items = donation_data.get("items") or []

        # traz o validador IN para a criação para evitar lentidão
        if items:
            requested_product_ids = [item["product_id"] for item in items]
            existing_products = await self.product_repository.get_by_ids(db, requested_product_ids)
            existing_ids = {product.product_id for product in existing_products}
            
            missing_ids = set(requested_product_ids) - existing_ids
            if missing_ids:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Os seguintes produtos não foram encontrados: {list(missing_ids)}"
                )

        async with db.begin():
            return await self.repository.create(db, donation_data)

    async def list_donations(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_donation(self, db: AsyncSession, donation_id: int):
        donation = await self.repository.get_by_id(db, donation_id)
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doação não encontrada")
        return donation

    async def delete_donation(self, db: AsyncSession, donation_id: int):
        # no futuro, o delete precisará chamar o InventoryService
        # para subtrair os produtos do estoque antes de apagar a doação.
        async with db.begin():
            donation = await self.repository.delete(db, donation_id)
            if not donation:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doação não encontrada")
            return donation
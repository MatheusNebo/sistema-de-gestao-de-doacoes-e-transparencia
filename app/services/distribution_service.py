from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.distribution import Distribution
from app.repositories.distribution_repository import DistributionRepository
from app.repositories.beneficiary_repository import BeneficiaryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.distribution_schema import DistributionCreate

class DistributionService:
    def __init__(self):
        self.repository = DistributionRepository()
        self.beneficiary_repository = BeneficiaryRepository() # Você precisará disso
        self.product_repository = ProductRepository()

    async def create_distribution(self, db: AsyncSession, data: DistributionCreate):
        # valida se o Beneficiário existe
        beneficiary = await self.beneficiary_repository.get_by_id(db, data.beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=404, detail="Beneficiário não encontrado")

        distribution_data = data.model_dump()
        items = distribution_data.get("items", [])

        # valida se todos os produtos existem de uma só vez (Cláusula IN)
        requested_product_ids = [item["product_id"] for item in items]
        existing_products = await self.product_repository.get_by_ids(db, requested_product_ids)
        existing_ids = {product.product_id for product in existing_products}
        
        missing_ids = set(requested_product_ids) - existing_ids
        if missing_ids:
            raise HTTPException(
                status_code=404,
                detail=f"Produtos não encontrados: {list(missing_ids)}"
            )

        # futuramente aqui: Validar se TEM ESTOQUE antes de distribuir (InventoryService)

        async with db.begin():
            return await self.repository.create(db, distribution_data)
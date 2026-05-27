from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.distribution import Distribution
from app.repositories.distribution_repository import DistributionRepository
from app.repositories.beneficiary_repository import BeneficiaryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.distribution_schema import DistributionCreate
from app.services.inventory_service import InventoryService
from app.schemas.inventory_movement_schema import InventoryMovementCreate
from app.exceptions import DomainError

class DistributionService:
    def __init__(self):
        # instancia os repositórios necessários
        self.repository = DistributionRepository()
        self.beneficiary_repository = BeneficiaryRepository()
        self.product_repository = ProductRepository()
        self.inventory_service = InventoryService()

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

        try:
            # transação principal 
            async with db.begin():
                # cria a distribuição e os DistributionItems no banco
                distribution = await self.repository.create(db, distribution_data)

                # para cada item distribuído, manda a ordem de saída para o estoque
                for item in items:
                    movement_data = InventoryMovementCreate(
                        product_id=item["product_id"],
                        quantity=item["quantity"],
                        movement_type="saida",        # <-- saída de estoque
                        source="distribuicao",        # <-- origem: distribuição
                        beneficiary_id=distribution.beneficiary_id # <-- vínculo histórico
                    )

                    # o InventoryService vai validar o saldo e rodar o FIFO de lotes automaticamente.
                    # como é Saída, não passamos batch e nem expiration_date (o FIFO descobre sozinho).
                    await self.inventory_service.register_movement(
                        db=db,
                        movement_data=movement_data
                    )

                return distribution

        except DomainError as e:
            # captura o erro de falta de estoque lançado pelo InventoryService
            # e converte em um erro HTTP 400 amigável para o front-end
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            # repassa outros erros genéricos para o handler global 500
            raise e
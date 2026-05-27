from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.donation_repository import DonationRepository
from app.repositories.donor_repository import DonorRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.donation_schema import DonationCreate
from app.enums import DonationType

# IMPORTAMOS O INVENTORY SERVICE E O SCHEMA DO MOVIMENTO
from app.services.inventory_service import InventoryService
from app.schemas.inventory_movement_schema import InventoryMovementCreate

class DonationService:

    def __init__(self):
        self.repository = DonationRepository()
        self.donor_repository = DonorRepository()
        self.product_repository = ProductRepository()
        # Instancia o serviço de estoque
        self.inventory_service = InventoryService() 

    async def create_donation(self, db: AsyncSession, data: DonationCreate):
        # valida Doador
        donor = await self.donor_repository.get_by_id(db, data.donor_id)
        if not donor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doador não encontrado")

        donation_data = data.model_dump()
        items = donation_data.get("items") or []

        # valida Produtos (cláusula IN otimizada)
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

        # valida Lote e Validade para Alimentos
        if data.donation_type == DonationType.FOOD:
            for item in items:
                if not item.get("batch") or not item.get("expiration_date"):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Lote e data de validade são obrigatórios para doações de alimentos."
                    )

        # transação principal 
        async with db.begin():
            # cria a doação e os DonationItems no banco
            donation = await self.repository.create(db, donation_data)

            # para cada item doado, manda para o estoque
            for item in items:
                movement_data = InventoryMovementCreate(
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    movement_type="entrada",
                    source="doacao",
                    donor_id=donation.donor_id
                )

                # chama o estoque separando o schema de log dos dados físicos
                await self.inventory_service.register_movement(
                    db=db,
                    movement_data=movement_data,
                    batch=item.get("batch"),
                    expiration_date=item.get("expiration_date")
                )

            return donation

    async def list_donations(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_donation(self, db: AsyncSession, donation_id: int):
        donation = await self.repository.get_by_id(db, donation_id)
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doação não encontrada")
        return donation

    async def delete_donation(self, db: AsyncSession, donation_id: int):
        # busca a doação ANTES de abrir a transação
        # precisamos dos dados dela e de seus itens para saber o que reverter
        donation = await self.repository.get_by_id(db, donation_id)
        if not donation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doação não encontrada")

        async with db.begin():
            # reverte o estoque caso a doação tenha itens
            # assumindo que donation.items traz a lista populada pelo SQLAlchemy (relationship)
            if donation.items:
                for item in donation.items:
                    # monta um movimento de SAÍDA para cancelar a entrada original
                    movement_data = InventoryMovementCreate(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        movement_type="saida",
                        source="ajuste", # 'ajuste' indica que é uma correção do sistema, não uma distribuição normal
                        donor_id=donation.donor_id
                    )

                    # chama o InventoryService para processar a baixa.
                    # vai automaticamente usar a lógica FIFO para remover os itens.
                    await self.inventory_service.register_movement(
                        db=db,
                        movement_data=movement_data
                    )

            # após garantir que o estoque foi revertido, apagamos a doação do banco
            await self.repository.delete(db, donation_id)
            
            return donation
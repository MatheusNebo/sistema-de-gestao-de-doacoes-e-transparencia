from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.beneficiary_repository import BeneficiaryRepository
from app.schemas.beneficiary_schema import BeneficiaryCreate, BeneficiaryUpdate
from app.services.audit_service import AuditService
from fastapi.encoders import jsonable_encoder

class BeneficiaryService:
    def __init__(self):
        self.repository = BeneficiaryRepository()
        self.audit_service = AuditService()

    async def create_beneficiary(self, db: AsyncSession, data: BeneficiaryCreate):
        # verifica se o CPF já está cadastrado
        existing_beneficiary = await self.repository.get_by_cpf(db, data.cpf)
        if existing_beneficiary:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Já existe um beneficiário cadastrado com este CPF."
            )

                # mantém os dados originais (com objetos datetime.date que o SQLAlchemy precisa)
        beneficiary_data = data.model_dump()

        # cria o beneficiário no banco primeiro usando os dados nativos
        beneficiary = await self.repository.create(db, beneficiary_data)

        # transforma em formato amigável para JSON EXCLUSIVAMENTE para a auditoria
        audit_data = jsonable_encoder(beneficiary_data)

        # registra na auditoria usando o 'audit_data' convertido
        await self.audit_service.log_create(
            db,
            entity_type="beneficiary",
            entity_id=beneficiary.beneficiary_id, 
            new_value=audit_data
        )

        # salva tudo de vez no banco
        await db.commit()
        return beneficiary

    async def list_beneficiaries(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_beneficiary(self, db: AsyncSession, beneficiary_id: int):
        beneficiary = await self.repository.get_by_id(db, beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiário não encontrado.")
        return beneficiary

    async def update_beneficiary(self, db: AsyncSession, beneficiary_id: int, data: BeneficiaryUpdate):
        # verifica se existe antes de tentar atualizar
        beneficiary = await self.repository.get_by_id(db, beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiário não encontrado.")

        # extrai APENAS os campos que o usuário enviou na requisição (ignora os Nulos não enviados)
        update_data = data.model_dump(exclude_unset=True)

        # se não enviou nada para atualizar, apenas retorna o próprio beneficiário
        if not update_data:
            return beneficiary

        # guarda valor antigo para auditoria
        old_value = {
            "name": beneficiary.name,
            "email": beneficiary.email,
            "birth_date": beneficiary.birth_date.isoformat() if beneficiary.birth_date else None,
            "address": beneficiary.address,
            "city": beneficiary.city,
            "telephone": beneficiary.telephone,
            "household_size": beneficiary.household_size,
            "family_income": float(beneficiary.family_income) if beneficiary.family_income else None,
        }

        # salva a atualização
        async with db.begin():
            updated = await self.repository.update(db, beneficiary_id, update_data)
            
            # registra na auditoria
            await self.audit_service.log_update(
                db,
                entity_type="beneficiary",
                entity_id=beneficiary_id,
                old_value=old_value,
                new_value=update_data
            )
            
            return updated

    async def delete_beneficiary(self, db: AsyncSession, beneficiary_id: int):
        beneficiary = await self.repository.get_by_id(db, beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Beneficiário não encontrado.")

        # guarda dados para auditoria
        old_value = {
            "beneficiary_id": beneficiary.beneficiary_id,
            "name": beneficiary.name,
            "cpf": beneficiary.cpf,
            "email": beneficiary.email,
            "birth_date": beneficiary.birth_date.isoformat() if beneficiary.birth_date else None,
            "address": beneficiary.address,
            "city": beneficiary.city,
            "telephone": beneficiary.telephone,
            "household_size": beneficiary.household_size,
            "family_income": float(beneficiary.family_income) if beneficiary.family_income else None,
        }

        async with db.begin():
            await self.repository.delete(db, beneficiary_id)
            
            # registra na auditoria
            await self.audit_service.log_delete(
                db,
                entity_type="beneficiary",
                entity_id=beneficiary_id,
                old_value=old_value
            )
            
            return beneficiary
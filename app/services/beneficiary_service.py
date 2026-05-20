from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.beneficiary_repository import BeneficiaryRepository
from app.schemas.beneficiary_schema import BeneficiaryCreate, BeneficiaryUpdate

class BeneficiaryService:
    def __init__(self):
        self.repository = BeneficiaryRepository()

    async def create_beneficiary(self, db: AsyncSession, data: BeneficiaryCreate):
        # verifica se o CPF já está cadastrado
        existing_beneficiary = await self.repository.get_by_cpf(db, data.cpf)
        if existing_beneficiary:
            raise HTTPException(
                status_code=400, 
                detail="Já existe um beneficiário cadastrado com este CPF."
            )

        # converte o schema do Pydantic para um dicionário
        beneficiary_data = data.model_dump()

        # salva no banco de dados garantindo a transação
        async with db.begin():
            return await self.repository.create(db, beneficiary_data)

    async def list_beneficiaries(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_beneficiary(self, db: AsyncSession, beneficiary_id: int):
        beneficiary = await self.repository.get_by_id(db, beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=404, detail="Beneficiário não encontrado.")
        return beneficiary

    async def update_beneficiary(self, db: AsyncSession, beneficiary_id: int, data: BeneficiaryUpdate):
        # verifica se existe antes de tentar atualizar
        beneficiary = await self.repository.get_by_id(db, beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=404, detail="Beneficiário não encontrado.")

        # extrai APENAS os campos que o usuário enviou na requisição (ignora os Nulos não enviados)
        update_data = data.model_dump(exclude_unset=True)

        # se não enviou nada para atualizar, apenas retorna o próprio beneficiário
        if not update_data:
            return beneficiary

        # salva a atualização
        async with db.begin():
            return await self.repository.update(db, beneficiary_id, update_data)

    async def delete_beneficiary(self, db: AsyncSession, beneficiary_id: int):
        beneficiary = await self.repository.get_by_id(db, beneficiary_id)
        if not beneficiary:
            raise HTTPException(status_code=404, detail="Beneficiário não encontrado.")

        async with db.begin():
            return await self.repository.delete(db, beneficiary_id)
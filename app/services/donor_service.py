from fastapi import HTTPException
from app.enums import DonorType
from app.repositories.donor_repository import DonorRepository
from sqlalchemy.ext.asyncio import AsyncSession


class DonorService:

    def __init__(self):
        self.repository = DonorRepository()

    async def create_donor(self, db: AsyncSession, data):
        self._validate_pf_pj(data)
        async with db.begin():
            return await self.repository.create(db, data)

    async def list_donors(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def get_donor(self, db: AsyncSession, donor_id: int):
        return await self.repository.get_by_id(db, donor_id)

    async def update_donor(self, db: AsyncSession, donor_id: int, data):
        current_donor = await self.repository.get_by_id(db, donor_id)
        if not current_donor:
            raise HTTPException(status_code=404, detail="Doador não encontrado")
        
        self._validate_pf_pj_update(data, current_donor)
        
        # converte o schema para dict contendo APENAS o que o usuário preencheu no payload
        update_data = data.model_dump(exclude_unset=True)
        
        async with db.begin():
            return await self.repository.update(db, donor_id, update_data)
        
        self._validate_pf_pj_update(data, current_donor)
        async with db.begin():
            return await self.repository.update(db, donor_id, data)

    async def delete_donor(self, db: AsyncSession, donor_id: int):
        async with db.begin():
            return await self.repository.delete(db, donor_id)

# validações específicas para doadores PF e PJ (não precisam de async por não executarem operações de banco)
    def _validate_pf_pj(self, data):
        if data.donor_type == DonorType.PF:
            if not data.name or not data.cpf:
                raise HTTPException(
                    status_code=400,
                    detail="Pessoa física exige nome e CPF"
                )

        elif data.donor_type == DonorType.PJ:
            if not data.company_name or not data.cnpj:
                raise HTTPException(
                    status_code=400,
                    detail="Pessoa jurídica exige razão social e CNPJ"
                )

    def _validate_pf_pj_update(self, data, current_donor):
        # bloqueia a mudança explícita de tipo de doador
        if data.donor_type and data.donor_type != current_donor.donor_type:
            raise HTTPException(
                status_code=400,
                detail="Não é permitido alterar o tipo de doador após a criação"
            )

        # usa o tipo atual do banco como verdade caso o update não envie o tipo
        active_type = data.donor_type or current_donor.donor_type

        # garante a integridade dos campos com base no tipo ativo do doador
        if active_type == DonorType.PF:
            if data.company_name or data.cnpj:
                raise HTTPException(
                    status_code=400,
                    detail="Pessoa física não deve possuir razão social ou CNPJ"
                )
        elif active_type == DonorType.PJ:
            if data.name or data.cpf:
                raise HTTPException(
                    status_code=400,
                    detail="Pessoa jurídica não deve possuir nome pessoal ou CPF"
                )

        # garante que campos de identificação nacional sejam imutáveis
        if data.cpf and data.cpf != current_donor.cpf:
            raise HTTPException(
                status_code=400,
                detail="CPF não pode ser alterado"
            )

        if data.cnpj and data.cnpj != current_donor.cnpj:
            raise HTTPException(
                status_code=400,
                detail="CNPJ não pode ser alterado"
            )

        
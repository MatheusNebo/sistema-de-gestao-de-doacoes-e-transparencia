from sqlalchemy.ext.asyncio import AsyncSession
from app.models.beneficiary import Beneficiary
from sqlalchemy import select

class BeneficiaryRepository:
    
    async def create(self, db: AsyncSession, data: dict):
        # recebe um dicionário (gerado pelo model_dump do Service) e cria a entidade
        db_beneficiary = Beneficiary(**data) # o ** desempacota o dicionário automaticamente
        db.add(db_beneficiary)
        await db.flush()
        await db.refresh(db_beneficiary)
        return db_beneficiary

    async def get_by_id(self, db: AsyncSession, beneficiary_id: int):
        result = await db.execute(
            select(Beneficiary).where(Beneficiary.beneficiary_id == beneficiary_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_cpf(self, db: AsyncSession, cpf: str):
        # busca por CPF para evitar duplicidades no cadastro
        result = await db.execute(
            select(Beneficiary).where(Beneficiary.cpf == cpf)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Beneficiary))
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, beneficiary_id: int, data: dict):
        # atualiza dinamicamente apenas as colunas que vieram no dicionário
        beneficiary = await self.get_by_id(db, beneficiary_id)
        if not beneficiary:
            return None
        
        # dinâmico: para cada chave/valor no dict, atualiza o atributo correspondente
        for key, value in data.items():
            setattr(beneficiary, key, value)

        await db.flush()
        await db.refresh(beneficiary)
        return beneficiary
    
    async def delete(self, db: AsyncSession, beneficiary_id: int):
        beneficiary = await self.get_by_id(db, beneficiary_id)
        if not beneficiary:
            return None
        
        await db.delete(beneficiary)
        await db.flush()
        return beneficiary
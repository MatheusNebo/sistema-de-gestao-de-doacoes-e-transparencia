from sqlalchemy.ext.asyncio import AsyncSession
from app.models.beneficiary import Beneficiary
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class BeneficiaryRepository:
    async def create(self, db: AsyncSession, data):
        db_beneficiary = Beneficiary(
            name=data.name,
            email=data.email,
            phone=data.phone,
            address=data.address
        )
        db.add(db_beneficiary)
        await db.flush()
        await db.refresh(db_beneficiary)
        return db_beneficiary

    async def get_by_id(self, db: AsyncSession, beneficiary_id: int):
        result = await db.execute(
            select(Beneficiary).where(Beneficiary.beneficiary_id == beneficiary_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Beneficiary))
        return result.scalars().all()
    
    async def update(self, db: AsyncSession, beneficiary_id: int, data):
        beneficiary = await self.get_by_id(db, beneficiary_id)
        if not beneficiary:
            return None
        
        beneficiary.name = data.name
        beneficiary.email = data.email
        beneficiary.phone = data.phone
        beneficiary.address = data.address

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
    
    
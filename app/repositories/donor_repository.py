from sqlalchemy.ext.asyncio import AsyncSession
from app.models.donor import Donor
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class DonorRepository:

    async def create(self, db: AsyncSession, data):
        donor = Donor(**data.model_dump())
        db.add(donor)
        await db.flush()
        await db.refresh(donor)
        return donor

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Donor))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, donor_id: int):
        result = await db.execute(
            select(Donor).where(Donor.donor_id == donor_id)
        )
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, donor_id: int, data):
        update_data = data.model_dump(exclude_unset=True)
    
        if not update_data:
            return await self.get_by_id(db, donor_id)
    
        donor = await self.get_by_id(db, donor_id)
        if not donor:
            return None
            
        for key, value in update_data.items():
            setattr(donor, key, value)
    
        await db.flush()
        return await self.get_by_id(db, donor_id)

    async def delete(self, db: AsyncSession, donor_id: int):
        donor = await self.get_by_id(db, donor_id)

        if not donor:
            return None

        await db.delete(donor)
        await db.flush()
        return donor
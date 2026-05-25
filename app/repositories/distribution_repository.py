from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import Distribution, DistributionItem

class DistributionRepository:
    async def create(self, db: AsyncSession, data: dict):
        items_data = data.pop("items", [])
        
        distribution = Distribution(**data)
        db.add(distribution)
        await db.flush() # Gera o distribution_id
        
        for item in items_data:
            dist_item = DistributionItem(**item, distribution_id=distribution.distribution_id)
            db.add(dist_item)
            
        await db.flush()
        await db.refresh(distribution, attribute_names=["items"])
        return distribution

    async def get_by_id(self, db: AsyncSession, distribution_id: int):
        stmt = (
            select(Distribution)
            .options(selectinload(Distribution.items))
            .where(Distribution.distribution_id == distribution_id)
        )
        result = await db.execute(stmt)
        return result.scalars().first()
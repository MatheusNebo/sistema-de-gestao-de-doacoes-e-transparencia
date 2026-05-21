from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.donation import Donation
from app.models.donation_item import DonationItem


class DonationRepository:

    async def create(self, db: AsyncSession, data: dict):
        items_data = data.pop("items", None)
        donation = Donation(**data)
        db.add(donation)
        await db.flush()

        if items_data:
            for item_data in items_data:
                donation_item = DonationItem(**{**item_data, "donation_id": donation.donation_id})
                db.add(donation_item)
            await db.flush()

        await db.refresh(donation)
        return donation

    async def get_all(self, db: AsyncSession):
        result = await db.execute(
            select(Donation)
            .options(selectinload(Donation.items))
        )
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, donation_id: int):
        result = await db.execute(
            select(Donation)
            .where(Donation.donation_id == donation_id)
            .options(selectinload(Donation.items))
        )
        return result.scalar_one_or_none()

    async def delete(self, db: AsyncSession, donation_id: int):
        donation = await self.get_by_id(db, donation_id)
        if not donation:
            return None

        await db.delete(donation)
        await db.flush()
        return donation

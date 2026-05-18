from sqlalchemy import Column, Integer, Date, String, Numeric, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from app.enums import DonationType

class Donation(Base):
    __tablename__ = "donation"

    donation_id = Column(Integer, primary_key=True)
    donor_id = Column(Integer, ForeignKey("donor.donor_id"), nullable=False)

    donation_date = Column(Date, nullable=False)
    donation_type = Column(Enum(DonationType), nullable=False)
    total_value = Column(Numeric(10,2))

    __table_args__ = (
        CheckConstraint("donation_type IN ('food','financial')", name="chk_donation_type"),
    )

    donor = relationship("Donor")
    items = relationship("DonationItem", back_populates="donation")
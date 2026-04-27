from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Distribution(Base):
    __tablename__ = "distribution"

    distribution_id = Column(Integer, primary_key=True)

    beneficiary_id = Column(Integer, ForeignKey("beneficiary.beneficiary_id"), nullable=False)
    distribution_date = Column(Date, nullable=False)

    beneficiary = relationship("Beneficiary")
    items = relationship("DistributionItem", back_populates="distribution")
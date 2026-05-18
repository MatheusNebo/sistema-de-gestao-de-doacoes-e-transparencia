from sqlalchemy import Column, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class DonationItem(Base):
    __tablename__ = "donation_item"

    donation_item_id = Column(Integer, primary_key=True)

    donation_id = Column(Integer, ForeignKey("donation.donation_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)

    quantity = Column(Numeric(10,2), nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_donation_item_quantity"),
    )

    donation = relationship("Donation", back_populates="items")
    product = relationship("Product")
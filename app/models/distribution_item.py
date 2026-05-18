from sqlalchemy import Column, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class DistributionItem(Base):
    __tablename__ = "distribution_item"

    distribution_item_id = Column(Integer, primary_key=True)

    distribution_id = Column(Integer, ForeignKey("distribution.distribution_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)

    quantity = Column(Numeric(10,2), nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="chk_distribution_quantity"),
    )

    distribution = relationship("Distribution", back_populates="items")
    product = relationship("Product")
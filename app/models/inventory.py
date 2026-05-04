from sqlalchemy import Column, Integer, Numeric, String, Date, ForeignKey, CheckConstraint
from datetime import date
from app.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    quantity = Column(Numeric(10,2), nullable=False)

    batch = Column(String(50))
    expiration_date = Column(Date, nullable=False)
    entry_date = Column(Date, default=date.today, nullable=False)

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="chk_inventory_quantity"),
        CheckConstraint("expiration_date >= entry_date", name="chk_inventory_expiration"),
    )
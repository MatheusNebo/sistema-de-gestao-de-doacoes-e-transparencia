from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, CheckConstraint
from datetime import datetime
from app.database import Base

class InventoryMovement(Base):
    __tablename__ = "inventory_movement"

    inventory_movement_id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)

    movement_type = Column(String(20), nullable=False)
    quantity = Column(Numeric(10,2), nullable=False)
    movement_date = Column(DateTime, default=datetime.utcnow)

    source = Column(String(50))

    __table_args__ = (
        CheckConstraint("movement_type IN ('entry','exit','loss')", name="chk_movement_type"),
        CheckConstraint("quantity > 0", name="chk_movement_quantity"),
        CheckConstraint("source IN ('donation','distribution','adjustment')", name="chk_movement_source"),
    )
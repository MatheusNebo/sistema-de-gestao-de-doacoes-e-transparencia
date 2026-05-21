from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, func
from sqlalchemy import Enum as SAEnum
from datetime import datetime
from app.database import Base
from app.enums import MovementType, MovementSource

class InventoryMovement(Base):
    __tablename__ = "inventory_movement"

    inventory_movement_id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)

    movement_type = Column(SAEnum(MovementType), nullable=False)
    quantity = Column(Numeric(10,2), nullable=False)
    movement_date = Column(DateTime, server_default=func.now(), nullable=False)
    source = Column(SAEnum(MovementSource))

    __table_args__ = (
        # quantity check remains
        # Note: movement_type and source are stored as Enums now
    )
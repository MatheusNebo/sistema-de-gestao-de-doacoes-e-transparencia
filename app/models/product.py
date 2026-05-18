from sqlalchemy import Column, Integer, String
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))
    unit = Column(String(20), nullable=False)
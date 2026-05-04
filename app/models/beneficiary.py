from sqlalchemy import Column, Integer, String, Date, Numeric, Text, CheckConstraint
from datetime import date
from app.database import Base

class Beneficiary(Base):
    __tablename__ = "beneficiary"

    beneficiary_id = Column(Integer, primary_key=True)

    name = Column(String(150), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)

    birth_date = Column(Date)
    address = Column(Text, nullable=False)
    city = Column(String(100))
    telephone = Column(String(20))

    household_size = Column(Integer)
    family_income = Column(Numeric(10,2))

    created_at = Column(Date, default=date.today)

    __table_args__ = (
        CheckConstraint("household_size > 0", name="chk_household_size"),
        CheckConstraint("family_income >= 0", name="chk_family_income"),
    )
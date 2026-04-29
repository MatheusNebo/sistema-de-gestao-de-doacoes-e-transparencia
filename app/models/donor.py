from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Enum
from datetime import datetime
from app.database import Base
from app.enums import DonorType

class Donor(Base):
    __tablename__ = "donor"

    donor_id = Column(Integer, primary_key=True)
    donor_type = Column(Enum(DonorType), nullable=False)

    name = Column(String(150))
    cpf = Column(String(14), unique=True)

    company_name = Column(String(150))
    cnpj = Column(String(18), unique=True)

    email = Column(String(150))
    phone = Column(String(20))

    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        CheckConstraint("donor_type IN ('PF','PJ')", name="chk_donor_type"),
        CheckConstraint("""
            (donor_type = 'PF' AND name IS NOT NULL AND cpf IS NOT NULL AND cnpj IS NULL AND company_name IS NULL)
            OR
            (donor_type = 'PJ' AND company_name IS NOT NULL AND cnpj IS NOT NULL AND cpf IS NULL AND name IS NULL)
        """, 
        name="chk_donor_pf_pj"),
    )
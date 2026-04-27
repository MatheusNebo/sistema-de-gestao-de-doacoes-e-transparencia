from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from app.database import Base

class SystemUser(Base):
    __tablename__ = "system_user"

    user_id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20))

    __table_args__ = (
        CheckConstraint("role IN ('admin','operator')", name="chk_user_role"),
    )
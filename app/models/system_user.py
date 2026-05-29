from sqlalchemy import Column, Integer, String, Text, CheckConstraint, Enum
from app.enums import UserRole
from app.database import Base

class SystemUser(Base):
    __tablename__ = "system_user"

    user_id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
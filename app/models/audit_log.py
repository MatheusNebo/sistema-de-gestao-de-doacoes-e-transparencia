from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, CheckConstraint, func
from sqlalchemy.types import JSON
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    audit_log_id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("system_user.user_id"), nullable=True)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)

    action = Column(String(20), nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "action IN ('CREATE', 'UPDATE', 'DELETE')",
            name="chk_action"
        ),
        CheckConstraint(
            "entity_type IN ('beneficiary', 'donor', 'product', 'donation', 'distribution', 'inventory')",
            name="chk_entity_type"
        ),
    )

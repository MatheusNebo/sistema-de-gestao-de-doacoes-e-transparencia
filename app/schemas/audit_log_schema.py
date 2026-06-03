from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class AuditLogBase(BaseModel):
    entity_type: str = Field(..., example="beneficiary")
    entity_id: int = Field(..., gt=0)
    action: str = Field(..., example="CREATE")
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None

class AuditLogResponse(AuditLogBase):
    audit_log_id: int
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AuditHistoryResponse(BaseModel):
    entity_type: str
    entity_id: int
    changes: list[AuditLogResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

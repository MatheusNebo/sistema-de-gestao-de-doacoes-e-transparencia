from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.audit_log_repository import AuditLogRepository
import json
from typing import Optional, Any, Dict

class AuditService:
    
    def __init__(self):
        self.repository = AuditLogRepository()

    async def log_create(
        self, 
        db: AsyncSession, 
        entity_type: str, 
        entity_id: int, 
        new_value: Dict[str, Any],
        user_id: Optional[int] = None
    ):
        """Registra criação de entidade"""
        audit_data = {
            "user_id": user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": "CREATE",
            "old_value": None,
            "new_value": self._serialize_value(new_value)
        }
        return await self.repository.create(db, audit_data)

    async def log_update(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: int,
        old_value: Dict[str, Any],
        new_value: Dict[str, Any],
        user_id: Optional[int] = None
    ):
        """Registra atualização de entidade"""
        audit_data = {
            "user_id": user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": "UPDATE",
            "old_value": self._serialize_value(old_value),
            "new_value": self._serialize_value(new_value)
        }
        return await self.repository.create(db, audit_data)

    async def log_delete(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: int,
        old_value: Dict[str, Any],
        user_id: Optional[int] = None
    ):
        """Registra deleção de entidade"""
        audit_data = {
            "user_id": user_id,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "action": "DELETE",
            "old_value": self._serialize_value(old_value),
            "new_value": None
        }
        return await self.repository.create(db, audit_data)

    async def get_entity_history(self, db: AsyncSession, entity_type: str, entity_id: int):
        """Retorna histórico completo de uma entidade"""
        return await self.repository.get_by_entity(db, entity_type, entity_id)

    async def get_user_actions(self, db: AsyncSession, user_id: int, limit: int = 50):
        """Retorna últimas ações de um usuário"""
        return await self.repository.get_by_user(db, user_id, limit)

    async def get_recent_audits(self, db: AsyncSession, limit: int = 100):
        """Retorna registros de auditoria recentes"""
        return await self.repository.get_all(db, limit)

    @staticmethod
    def _serialize_value(value: Any) -> Optional[Dict]:
        """Serializa valor para JSON, removendo campos sensíveis"""
        if not value:
            return None
        
        if isinstance(value, dict):
            # Remove password_hash de registros de user
            serializable = value.copy()
            if "password_hash" in serializable:
                del serializable["password_hash"]
            return serializable
        
        return None

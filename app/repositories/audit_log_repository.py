from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models.audit_log import AuditLog

class AuditLogRepository:
    
    async def create(self, db: AsyncSession, data: dict):
       # registra um novo evento de auditoria
        audit = AuditLog(**data)
        db.add(audit)
        await db.flush()
        await db.refresh(audit)
        return audit

    async def get_by_id(self, db: AsyncSession, audit_log_id: int):
        # busca um registro de auditoria por ID
        result = await db.execute(
            select(AuditLog).where(AuditLog.audit_log_id == audit_log_id)
        )
        return result.scalar_one_or_none()

    async def get_by_entity(self, db: AsyncSession, entity_type: str, entity_id: int):
        # busca histórico de auditoria de uma entidade específica
        result = await db.execute(
            select(AuditLog)
            .where(
                (AuditLog.entity_type == entity_type) &
                (AuditLog.entity_id == entity_id)
            )
            .order_by(desc(AuditLog.created_at))
        )
        return result.scalars().all()

    async def get_by_user(self, db: AsyncSession, user_id: int, limit: int = 50):
        # busca auditoria por usuário (últimas N ações)
        result = await db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
        )
        return result.scalars().all()

    async def get_all(self, db: AsyncSession, limit: int = 100):
        # busca todos os registros de auditoria (com limit)
        result = await db.execute(
            select(AuditLog)
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
        )
        return result.scalars().all()

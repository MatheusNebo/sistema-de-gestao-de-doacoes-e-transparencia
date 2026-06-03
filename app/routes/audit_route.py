from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.services.audit_service import AuditService

router = APIRouter(prefix="/audits", tags=["Audits"])

service = AuditService()

@router.get("/")
async def get_recent_audits(
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    
    # retorna registros de auditoria recentes (últimas ações do sistema).
    
    # **limit**: Número de registros a retornar (padrão: 100, máximo: 500)

    return await service.get_recent_audits(db, limit)

@router.get("/entity/{entity_type}/{entity_id}")
async def get_entity_history(
    entity_type: str,
    entity_id: int,
    db: AsyncSession = Depends(get_db)
):
    
    # retorna histórico completo de alterações de uma entidade.
    
    # **entity_type**: Tipo da entidade (beneficiary, donor, product, donation, distribution, inventory)
    # **entity_id**: ID da entidade

    if entity_type not in ['beneficiary', 'donor', 'product', 'donation', 'distribution', 'inventory']:
        raise HTTPException(status_code=400, detail="Tipo de entidade inválido")
    
    history = await service.get_entity_history(db, entity_type, entity_id)
    return history

@router.get("/user/{user_id}")
async def get_user_actions(
    user_id: int,
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    
    # retorna últimas ações de um usuário específico.
    
    # **user_id**: ID do usuário
    # **limit**: Número de registros a retornar (padrão: 50, máximo: 500)
    
    actions = await service.get_user_actions(db, user_id, limit)
    if not actions:
        return []
    return actions

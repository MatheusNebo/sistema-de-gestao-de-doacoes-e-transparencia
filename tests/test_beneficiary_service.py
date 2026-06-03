"""
test_beneficiary_service.py - Testes para BeneficiaryService
Valida: CRUD, auditoria, validações
"""

import pytest
from datetime import datetime
from fastapi import HTTPException
from app.services.beneficiary_service import BeneficiaryService
from app.schemas.beneficiary_schema import BeneficiaryCreate, BeneficiaryUpdate


@pytest.mark.asyncio
class TestBeneficiaryService:
    
    @pytest.fixture
    def service(self):
        return BeneficiaryService()
    
    async def test_create_beneficiary_success(self, service, db_session, beneficiary_data):
        """✅ Criar beneficiário com sucesso"""
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        
        assert beneficiary is not None
        assert beneficiary.name == "João Silva"
        assert beneficiary.email == "joao@example.com"
        assert beneficiary.birth_date is not None
    
    async def test_beneficiary_birth_date_not_null(self, service, db_session):
        """✅ birth_date é obrigatório (NOT NULL)"""
        # Tentar criar sem birth_date deve falhar
        invalid_data = {
            "name": "Teste",
            "email": "teste@example.com",
            "phone": "1133334444"
            # falta birth_date
        }
        
        # Pydantic deve rejeitar antes de chegar ao service
        with pytest.raises(Exception):
            BeneficiaryCreate(**invalid_data)
    
    async def test_list_beneficiaries(self, service, db_session, beneficiary_data):
        """✅ Listar beneficiários"""
        schema = BeneficiaryCreate(**beneficiary_data)
        await service.create_beneficiary(db_session, schema)
        
        beneficiaries = await service.list_beneficiaries(db_session)
        assert len(beneficiaries) >= 1
    
    async def test_get_beneficiary_by_id(self, service, db_session, beneficiary_data):
        """✅ Buscar beneficiário por ID"""
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        
        fetched = await service.get_beneficiary(db_session, beneficiary.beneficiary_id)
        assert fetched is not None
        assert fetched.beneficiary_id == beneficiary.beneficiary_id
    
    async def test_update_beneficiary(self, service, db_session, beneficiary_data):
        """✅ Atualizar beneficiário"""
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        
        update_data = BeneficiaryUpdate(name="Maria Silva")
        updated = await service.update_beneficiary(db_session, beneficiary.beneficiary_id, update_data)
        
        assert updated.name == "Maria Silva"
    
    async def test_delete_beneficiary(self, service, db_session, beneficiary_data):
        """✅ Deletar beneficiário"""
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        
        deleted = await service.delete_beneficiary(db_session, beneficiary.beneficiary_id)
        assert deleted is not None
        
        # Verificar que foi deletado
        fetched = await service.get_beneficiary(db_session, beneficiary.beneficiary_id)
        assert fetched is None
    
    async def test_audit_log_on_create(self, service, db_session, beneficiary_data):
        """✅ Auditoria: registrar CREATE ao criar beneficiário"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        
        audits = await audit_repo.get_by_entity(db_session, "beneficiary", beneficiary.beneficiary_id)
        assert len(audits) > 0
        assert audits[0].action == "CREATE"
    
    async def test_audit_log_on_update(self, service, db_session, beneficiary_data):
        """✅ Auditoria: registrar UPDATE ao modificar beneficiário"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        
        update_data = BeneficiaryUpdate(name="Novo Nome")
        await service.update_beneficiary(db_session, beneficiary.beneficiary_id, update_data)
        
        audits = await audit_repo.get_by_entity(db_session, "beneficiary", beneficiary.beneficiary_id)
        update_audit = [a for a in audits if a.action == "UPDATE"]
        assert len(update_audit) > 0
    
    async def test_audit_log_on_delete(self, service, db_session, beneficiary_data):
        """✅ Auditoria: registrar DELETE ao remover beneficiário"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = BeneficiaryCreate(**beneficiary_data)
        beneficiary = await service.create_beneficiary(db_session, schema)
        beneficiary_id = beneficiary.beneficiary_id
        
        await service.delete_beneficiary(db_session, beneficiary_id)
        
        audits = await audit_repo.get_by_entity(db_session, "beneficiary", beneficiary_id)
        delete_audit = [a for a in audits if a.action == "DELETE"]
        assert len(delete_audit) > 0

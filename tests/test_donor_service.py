"""
test_donor_service.py - Testes para DonorService
Valida: CRUD, donor_type, constraints, auditoria
"""

import pytest
from fastapi import HTTPException
from app.services.donor_service import DonorService
from app.schemas.donor_schema import DonorCreate, DonorUpdate
from app.enums import DonationType


@pytest.mark.asyncio
class TestDonorService:
    
    @pytest.fixture
    def service(self):
        return DonorService()
    
    async def test_create_donor_legal_person(self, service, db_session, donor_data):
        """✅ Criar doador pessoa jurídica com CNPJ"""
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        
        assert donor is not None
        assert donor.name == "Empresa XYZ"
        assert donor.donor_type == DonationType.LEGAL_PERSON
        assert donor.cnpj_cpf == "12345678000100"
    
    async def test_create_donor_individual(self, service, db_session):
        """✅ Criar doador pessoa física com CPF"""
        data = {
            "name": "Pedro da Silva",
            "email": "pedro@example.com",
            "phone": "11987654321",
            "donor_type": "INDIVIDUAL",
            "cnpj_cpf": "12345678900"
        }
        schema = DonorCreate(**data)
        donor = await service.create_donor(db_session, schema)
        
        assert donor.donor_type == DonationType.INDIVIDUAL
    
    async def test_create_donor_individual_invalid_cpf(self, service, db_session):
        """❌ CPF com formato inválido deve ser rejeitado"""
        data = {
            "name": "João",
            "email": "joao@example.com",
            "phone": "1133334444",
            "donor_type": "INDIVIDUAL",
            "cnpj_cpf": "invalid"
        }
        
        # Validação de CPF/CNPJ deve rejeitar
        with pytest.raises(Exception):
            await service.create_donor(db_session, DonorCreate(**data))
    
    async def test_list_donors(self, service, db_session, donor_data):
        """✅ Listar doadores"""
        schema = DonorCreate(**donor_data)
        await service.create_donor(db_session, schema)
        
        donors = await service.list_donors(db_session)
        assert len(donors) >= 1
    
    async def test_get_donor_by_id(self, service, db_session, donor_data):
        """✅ Buscar doador por ID"""
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        
        fetched = await service.get_donor(db_session, donor.donor_id)
        assert fetched is not None
        assert fetched.donor_id == donor.donor_id
    
    async def test_update_donor(self, service, db_session, donor_data):
        """✅ Atualizar doador"""
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        
        update_data = DonorUpdate(email="newemail@xyz.com")
        updated = await service.update_donor(db_session, donor.donor_id, update_data)
        
        assert updated.email == "newemail@xyz.com"
    
    async def test_delete_donor(self, service, db_session, donor_data):
        """✅ Deletar doador"""
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        
        deleted = await service.delete_donor(db_session, donor.donor_id)
        assert deleted is not None
        
        fetched = await service.get_donor(db_session, donor.donor_id)
        assert fetched is None
    
    async def test_audit_log_on_create(self, service, db_session, donor_data):
        """✅ Auditoria: registrar CREATE ao criar doador"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        
        audits = await audit_repo.get_by_entity(db_session, "donor", donor.donor_id)
        assert len(audits) > 0
        assert audits[0].action == "CREATE"
        assert audits[0].new_value is not None
    
    async def test_audit_log_on_update(self, service, db_session, donor_data):
        """✅ Auditoria: registrar UPDATE com old_value e new_value"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        
        update_data = DonorUpdate(email="novo@email.com")
        await service.update_donor(db_session, donor.donor_id, update_data)
        
        audits = await audit_repo.get_by_entity(db_session, "donor", donor.donor_id)
        update_audit = [a for a in audits if a.action == "UPDATE"]
        assert len(update_audit) > 0
        assert update_audit[0].old_value is not None  # Deve ter valor antigo
        assert update_audit[0].new_value is not None  # Deve ter valor novo
    
    async def test_audit_log_on_delete(self, service, db_session, donor_data):
        """✅ Auditoria: registrar DELETE com valores deletados"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = DonorCreate(**donor_data)
        donor = await service.create_donor(db_session, schema)
        donor_id = donor.donor_id
        
        await service.delete_donor(db_session, donor_id)
        
        audits = await audit_repo.get_by_entity(db_session, "donor", donor_id)
        delete_audit = [a for a in audits if a.action == "DELETE"]
        assert len(delete_audit) > 0
        assert delete_audit[0].old_value is not None  # Deve ter valores deletados

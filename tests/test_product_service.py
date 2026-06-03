"""
test_product_service.py - Testes para ProductService
Valida: CRUD, normalização de nome/unit, constraints
"""

import pytest
from fastapi import HTTPException
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
class TestProductService:
    
    @pytest.fixture
    def service(self):
        return ProductService()
    
    async def test_create_product_success(self, service, db_session, product_data):
        """✅ Criar produto com sucesso"""
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        
        assert product is not None
        assert product.name == "Arroz Integral"  # Deve ser title case
        assert product.unit == "kg"
        assert product.category == "FOOD"
    
    async def test_create_product_normalize_name(self, service, db_session):
        """✅ Normalizar nome para title case"""
        data = ProductCreate(name="arroz integral", category="FOOD", unit="kg")
        product = await service.create_product(db_session, data)
        
        assert product.name == "Arroz Integral"
    
    async def test_create_product_normalize_unit(self, service, db_session):
        """✅ Normalizar unidade para lowercase"""
        data = ProductCreate(name="Feijão", category="FOOD", unit="KG")
        product = await service.create_product(db_session, data)
        
        assert product.unit == "kg"
    
    async def test_create_duplicate_product_fails(self, service, db_session, product_data):
        """❌ Rejeitar produto duplicado (mesmo nome + unit)"""
        schema = ProductCreate(**product_data)
        
        # Criar primeiro
        await service.create_product(db_session, schema)
        
        # Tentar criar duplicado
        with pytest.raises(HTTPException) as exc:
            await service.create_product(db_session, schema)
        
        assert exc.value.status_code == 400
        assert "já está cadastrado" in exc.value.detail
    
    async def test_list_products(self, service, db_session, product_data):
        """✅ Listar produtos"""
        # Criar 2 produtos
        for i in range(2):
            data = ProductCreate(
                name=f"Produto {i}",
                category="FOOD",
                unit="kg"
            )
            await service.create_product(db_session, data)
        
        products = await service.list_products(db_session)
        assert len(products) >= 2
    
    async def test_get_product_by_id(self, service, db_session, product_data):
        """✅ Buscar produto por ID"""
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        
        fetched = await service.get_product(db_session, product.product_id)
        assert fetched is not None
        assert fetched.product_id == product.product_id
        assert fetched.name == product.name
    
    async def test_update_product(self, service, db_session, product_data):
        """✅ Atualizar produto"""
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        
        update_data = ProductUpdate(name="Arroz Branco")
        updated = await service.update_product(db_session, product.product_id, update_data)
        
        assert updated.name == "Arroz Branco"
    
    async def test_delete_product(self, service, db_session, product_data):
        """✅ Deletar produto"""
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        
        deleted = await service.delete_product(db_session, product.product_id)
        assert deleted is not None
        
        # Verificar que foi deletado
        fetched = await service.get_product(db_session, product.product_id)
        assert fetched is None
    
    async def test_audit_log_on_create(self, service, db_session, product_data):
        """✅ Auditoria: registrar CREATE ao criar produto"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        
        # Verificar se há registro de auditoria
        audits = await audit_repo.get_by_entity(db_session, "product", product.product_id)
        assert len(audits) > 0
        assert audits[0].action == "CREATE"
        assert audits[0].entity_type == "product"
    
    async def test_audit_log_on_update(self, service, db_session, product_data):
        """✅ Auditoria: registrar UPDATE ao modificar produto"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        
        # Atualizar
        update_data = ProductUpdate(name="Novo Nome")
        await service.update_product(db_session, product.product_id, update_data)
        
        # Verificar se há registro de UPDATE
        audits = await audit_repo.get_by_entity(db_session, "product", product.product_id)
        update_audit = [a for a in audits if a.action == "UPDATE"]
        assert len(update_audit) > 0
    
    async def test_audit_log_on_delete(self, service, db_session, product_data):
        """✅ Auditoria: registrar DELETE ao remover produto"""
        from app.repositories.audit_log_repository import AuditLogRepository
        audit_repo = AuditLogRepository()
        
        schema = ProductCreate(**product_data)
        product = await service.create_product(db_session, schema)
        product_id = product.product_id
        
        # Deletar
        await service.delete_product(db_session, product_id)
        
        # Verificar se há registro de DELETE
        audits = await audit_repo.get_by_entity(db_session, "product", product_id)
        delete_audit = [a for a in audits if a.action == "DELETE"]
        assert len(delete_audit) > 0

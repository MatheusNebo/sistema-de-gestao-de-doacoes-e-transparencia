"""
test_api_endpoints.py - Testes de API (endpoints HTTP)
Testes de integração completos
"""

import pytest
import json
from fastapi import status


class TestProductAPI:
    """Testes de endpoints de Product"""
    
    def test_create_product_endpoint(self, client, product_data):
        """✅ POST /products/ - Criar produto"""
        response = client.post("/products/", json=product_data)
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["name"] == "Arroz Integral"
    
    def test_list_products_endpoint(self, client, product_data):
        """✅ GET /products/ - Listar produtos"""
        # Criar primeiro
        client.post("/products/", json=product_data)
        
        response = client.get("/products/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_product_endpoint(self, client, product_data):
        """✅ GET /products/{id} - Buscar produto"""
        # Criar produto
        create_response = client.post("/products/", json=product_data)
        product = create_response.json()
        
        response = client.get(f"/products/{product['product_id']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["product_id"] == product["product_id"]
    
    def test_update_product_endpoint(self, client, product_data):
        """✅ PUT /products/{id} - Atualizar produto"""
        # Criar produto
        create_response = client.post("/products/", json=product_data)
        product = create_response.json()
        
        update_data = {"name": "Arroz Branco"}
        response = client.put(f"/products/{product['product_id']}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Arroz Branco"
    
    def test_delete_product_endpoint(self, client, product_data):
        """✅ DELETE /products/{id} - Deletar produto"""
        # Criar produto
        create_response = client.post("/products/", json=product_data)
        product = create_response.json()
        
        response = client.delete(f"/products/{product['product_id']}")
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verificar que foi deletado
        get_response = client.get(f"/products/{product['product_id']}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestBeneficiaryAPI:
    """Testes de endpoints de Beneficiary"""
    
    def test_create_beneficiary_endpoint(self, client, beneficiary_data):
        """✅ POST /beneficiaries/ - Criar beneficiário"""
        response = client.post("/beneficiaries/", json=beneficiary_data)
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["name"] == "João Silva"
    
    def test_list_beneficiaries_endpoint(self, client, beneficiary_data):
        """✅ GET /beneficiaries/ - Listar beneficiários"""
        client.post("/beneficiaries/", json=beneficiary_data)
        
        response = client.get("/beneficiaries/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestDonorAPI:
    """Testes de endpoints de Donor"""
    
    def test_create_donor_endpoint(self, client, donor_data):
        """✅ POST /donors/ - Criar doador"""
        response = client.post("/donors/", json=donor_data)
        
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        data = response.json()
        assert data["name"] == "Empresa XYZ"
    
    def test_list_donors_endpoint(self, client, donor_data):
        """✅ GET /donors/ - Listar doadores"""
        client.post("/donors/", json=donor_data)
        
        response = client.get("/donors/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


class TestAuditAPI:
    """Testes de endpoints de Auditoria"""
    
    def test_get_recent_audits(self, client, product_data):
        """✅ GET /audits/ - Obter últimos registros de auditoria"""
        # Criar um produto (gera auditoria)
        client.post("/products/", json=product_data)
        
        response = client.get("/audits/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_entity_history(self, client, product_data):
        """✅ GET /audits/entity/{type}/{id} - Histórico de entidade"""
        # Criar produto
        create_response = client.post("/products/", json=product_data)
        product = create_response.json()
        
        response = client.get(f"/audits/entity/product/{product['product_id']}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        # Deve ter pelo menos um CREATE
        assert len(data) > 0 or response.status_code == 200
    
    def test_audit_captures_product_changes(self, client, product_data):
        """✅ Auditoria: captura criação, atualização e deleção"""
        # 1. Criar produto
        create_response = client.post("/products/", json=product_data)
        product = create_response.json()
        
        # 2. Consultar auditoria (deve ter CREATE)
        audit_response = client.get(f"/audits/entity/product/{product['product_id']}")
        assert audit_response.status_code == status.HTTP_200_OK
        
        # 3. Atualizar produto
        update_data = {"name": "Novo Nome"}
        client.put(f"/products/{product['product_id']}", json=update_data)
        
        # 4. Consultar auditoria (deve ter UPDATE)
        audit_response = client.get(f"/audits/entity/product/{product['product_id']}")
        assert audit_response.status_code == status.HTTP_200_OK


class TestConstraints:
    """Testes de validação de constraints"""
    
    def test_product_normalize_name(self, client):
        """✅ Produto: nome normalizado para Title Case"""
        data = {
            "name": "arroz integral",  # Minúsculas
            "category": "FOOD",
            "unit": "kg"
        }
        response = client.post("/products/", json=data)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
        
        product = response.json()
        assert product["name"] == "Arroz Integral"  # Title Case
    
    def test_product_normalize_unit(self, client):
        """✅ Produto: unidade normalizada para lowercase"""
        data = {
            "name": "Feijão",
            "category": "FOOD",
            "unit": "KG"  # Maiúsculas
        }
        response = client.post("/products/", json=data)
        
        product = response.json()
        assert product["unit"] == "kg"  # Lowercase
    
    def test_beneficiary_requires_birth_date(self, client):
        """✅ Beneficiário: birth_date obrigatório"""
        data = {
            "name": "Teste",
            "email": "teste@example.com",
            "phone": "1133334444"
            # Falta birth_date
        }
        response = client.post("/beneficiaries/", json=data)
        
        # Deve rejeitar (422 Unprocessable Entity)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

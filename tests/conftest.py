"""
conftest.py - Configuração global de fixtures para testes pytest
Fornece: banco de dados de teste, cliente FastAPI, sessões async
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from app.database import Base, get_db

# Database test URL (SQLite in-memory para testes rápidos)
DATABASE_TEST_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """Cria engine de teste com SQLite em memória"""
    engine = create_async_engine(
        DATABASE_TEST_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(engine):
    """Cria sessão de teste para cada teste"""
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # NÃO iniciar transação aqui - deixa o service controlar
        yield session
        # Rollback de qualquer transação aberta
        try:
            await session.rollback()
        except:
            pass


@pytest.fixture(scope="function")
def override_get_db(db_session):
    """Override de dependency injection para usar sessão de teste"""
    async def _override():
        return db_session
    
    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(override_get_db):
    """Cliente FastAPI síncrono para testes"""
    return TestClient(app)


# ============================================================================
# Fixtures de dados de teste (factories)
# ============================================================================

@pytest.fixture
def product_data():
    """Dados de teste para Product"""
    return {
        "name": "Arroz Integral",
        "category": "FOOD",
        "unit": "kg"
    }


@pytest.fixture
def beneficiary_data():
    """Dados de teste para Beneficiary"""
    return {
        "name": "João Silva",
        "email": "joao@example.com",
        "phone": "11987654321",
        "birth_date": "1990-05-15"
    }


@pytest.fixture
def donor_data():
    """Dados de teste para Donor"""
    return {
        "name": "Empresa XYZ",
        "email": "contato@xyz.com",
        "phone": "1133334444",
        "donor_type": "LEGAL_PERSON",
        "cnpj_cpf": "12345678000100"
    }


@pytest.fixture
def inventory_data():
    """Dados de teste para Inventory"""
    return {
        "product_id": 1,
        "quantity": 100,
        "batch": "LOTE001",
        "expiration_date": "2026-12-31"
    }


@pytest.fixture
def donation_data():
    """Dados de teste para Donation"""
    return {
        "donor_id": 1,
        "donation_type": "FOOD",
        "items": [
            {
                "product_id": 1,
                "quantity": 50,
                "batch": "LOTE001",
                "expiration_date": "2026-12-31"
            }
        ]
    }


@pytest.fixture
def distribution_data():
    """Dados de teste para Distribution"""
    return {
        "beneficiary_id": 1,
        "items": [
            {
                "product_id": 1,
                "quantity": 20
            }
        ]
    }

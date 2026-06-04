from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL de conexão com o banco (com asyncpg driver)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:senha@localhost:5432/nome_do_banco"
)

# cria o engine assíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# cria a fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# base única para todos os models
Base = declarative_base()


# função para obter sessão assíncrona (usada no FastAPI)
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db


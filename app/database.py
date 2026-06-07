from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # carrega as variáveis de ambiente do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL de conexão com o banco
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123@localhost:5432/ong"
)

# Cria o engine (conexão com o banco)
engine = create_engine(
    DATABASE_URL,
    echo=False
)

# Cria a fábrica de sessões
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base única para todos os models
Base = declarative_base()


# Função para obter sessão (usada no FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# configuração do hash de senha (Bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

load_dotenv()  # carrega variáveis de ambiente do arquivo .env
# CONFIGURAÇÕES DO JWT (Em produção, mova para o seu arquivo .env)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # Token válido por 1 hora

def get_password_hash(password: str) -> str:
    # transforma a senha em texto puro em um Hash Bcrypt criptografado
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # verifica se a senha digitada bate com o hash salvo no banco
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # gera o Token JWT assinado para o usuário
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
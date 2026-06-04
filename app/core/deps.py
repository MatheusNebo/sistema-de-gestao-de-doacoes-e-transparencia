import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core import security

# indica ao FastAPI qual endpoint gera o token (habilita o botão do "Cadeado" no Swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    
    # dependencia que valida o JWT. Se o token for inválido, barra a requisiçao aqui mesmo.
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de autenticação inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # decodifica o Token usando a chave secreta
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
            
        # retornar um dicionário simples ou buscar o objeto User do banco aqui
        return {"email": email, "role": role}
        
    except jwt.PyJWTError:
        raise credentials_exception
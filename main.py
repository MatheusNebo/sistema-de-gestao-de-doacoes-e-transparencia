from fastapi import FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db 
from app.core import security

app = FastAPI()

from app.routes.auth_route import auth_router
from app.routes.product_route import router as product_router
from app.routes.donor_route import router as donor_router
from app.routes.beneficiary_route import router as beneficiary_router
from app.routes.inventory_route import router as inventory_router
from app.routes.inventory_movement_route import router as inventory_movement_router
from app.routes.distribution_route import router as distribution_router
from app.routes.donation_route import router as donation_router
from app.routes.audit_route import router as audit_router
from app.exceptions import domain_exception_handler, generic_exception_handler, DomainError

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(donor_router)
app.include_router(beneficiary_router)
app.include_router(inventory_router)
app.include_router(inventory_movement_router)
app.include_router(distribution_router)
app.include_router(donation_router)
app.include_router(audit_router)

# registra handlers globais para exceções de domínio e genéricas
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
async def read_root():
    return {"status": "Sistema de Gestão de Doações - Ativo"}

@app.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    # busca o usuário no banco (form_data.username conterá o email digitado)
    # user = await user_service.get_by_email(db, form_data.username)
    
    # simulação de validação (Substitua pela sua lógica real com o banco)
    user_exists = True # Exemplo dummy
    user_hashed_password = security.get_password_hash("123456") # Exemplo dummy
    
    if not user_exists or not security.verify_password(form_data.password, user_hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # gerar o Token incluindo informações úteis no payload (como a Role)
    access_token = security.create_access_token(
        data={"sub": "email_do_usuario@ong.com", "role": "admin"}
    )
    
    # o retorno PRECISA seguir este padrão do padrão OAuth2 para o Swagger funcionar
    return {"access_token": access_token, "token_type": "bearer"}
from fastapi import FastAPI

app = FastAPI()

from app.routes.auth_route import auth_router
from app.routes.product_route import router as product_router
from app.routes.donor_route import router as donor_router
from app.routes.inventory_route import router as inventory_router
from app.exceptions import domain_exception_handler, generic_exception_handler, DomainError

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(donor_router)
app.include_router(inventory_router)

# registra handlers globais para exceções de domínio e genéricas
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
async def read_root():
    return {"status": "Sistema de Gestão de Doações - Ativo"}


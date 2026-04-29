from fastapi import FastAPI 

app = FastAPI()

from app.routes.auth_routes import auth_router
from app.routes.product_routes import router as product_router

app.include_router(auth_router)
app.include_router(product_router)

@app.get("/")
def read_root():
    return {"status": "Sistema de Gestão de Doações - Ativo"}


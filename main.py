from fastapi import FastAPI 

app = FastAPI()

from routes.auth_routes import auth_router

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"status": "Sistema de Gestão de Doações - Ativo"}
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status


class DomainError(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "domain_error"

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}


class NotFoundError(DomainError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class ConflictError(DomainError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"


async def domain_exception_handler(request: Request, exc: DomainError):
    payload = {
        "code": exc.code,
        "message": exc.message,
        "details": exc.details,
    }
    return JSONResponse(status_code=exc.status_code, content=payload)


async def generic_exception_handler(request: Request, exc: Exception):
    #log de erro generico pode ser adicionado aqui para monitoramento
    payload = {
        "code": "internal_error",
        "message": "Erro interno no servidor",
    }
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload)

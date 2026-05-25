from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.domain.exceptions import (
    AppBaseException,
    ResourceNotFoundException,
    ValidationException,
    UnauthorizedException,
    InvalidAmountException,
    UnprocessableEntityException
)

async def domain_exception_handler(request: Request, exc: AppBaseException):
    status_mapping = {
        ResourceNotFoundException: 404,
        ValidationException: 400,
        InvalidAmountException: 400,
        UnprocessableEntityException: 422,
    }

    status_code = status_mapping.get(type(exc), 500)

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error_type": exc.__class__.__name__,
            "message": exc.message
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_type": "HttpException",
            "message": str(exc.detail)
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error_type": "ValidationError",
            "message": "Error in the data.",
            "details": exc.errors()
        }
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error_type": "Unauthorized",
            "message": exc.message
        },
        headers={"WWW-Authenticate": "Bearer"}
    )
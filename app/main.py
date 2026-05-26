# from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.presentation.api.v1.transaction_router import router as transaction_router
from app.presentation.api.v1.category_router import router as category_router
from app.presentation.api.v1.account_router import router as account_router
from app.presentation.api.v1.obligation_router import router as obligation_router
from app.presentation.api.v1.debt_router import router as debt_router
from app.presentation.api.v1.user_router import router as user_router

from app.domain.exceptions import AppBaseException, UnauthorizedException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.presentation.handlers import (
    domain_exception_handler, 
    http_exception_handler, 
    validation_exception_handler,
    unauthorized_exception_handler,
)
from asgi_correlation_id import CorrelationIdMiddleware
from app.core.logger import configure_logger, get_logger

load_dotenv()

configure_logger(is_production=os.getenv("PRODUCTION", False))

""" 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # I need the app create db and table since start.
    create_db_and_table()
    yield 
"""

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.add_middleware(CorrelationIdMiddleware)

logger = get_logger(__name__)
logger.info("api_started", version="1.0.0")

app.add_exception_handler(AppBaseException, domain_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)

app.include_router(transaction_router, prefix="/api/v1", tags=["transaction"])
app.include_router(category_router, prefix="/api/v1", tags=["category"])
app.include_router(account_router, prefix="/api/v1", tags=["account"])
app.include_router(obligation_router, prefix="/api/v1", tags=["obligation"])
app.include_router(debt_router, prefix="/api/v1", tags=["debt"])
app.include_router(user_router, prefix="/api/v1", tags=["user"])

@app.get("/")
def home() -> dict:
    return {"msg": "server is connect"}
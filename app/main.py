# from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.presentation.api.v1.transaction_router import router as transaction_router
from app.presentation.api.v1.category_router import router as category_router
from app.presentation.api.v1.account_router import router as account_router
from app.presentation.api.v1.obligation_router import router as obligation_router
from app.presentation.api.v1.debt_router import router as debt_router

""" 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # I need the app create db and table since start.
    create_db_and_table()
    yield 
"""

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(transaction_router, prefix="/api/v1", tags=["transaction"])
app.include_router(category_router, prefix="/api/v1", tags=["category"])
app.include_router(account_router, prefix="/api/v1", tags=["account"])
app.include_router(obligation_router, prefix="/api/v1", tags=["obligation"])
app.include_router(debt_router, prefix="/api/v1", tags=["debt"])

@app.get("/")
def home() -> dict:
    return {"msg": "server is connect"}
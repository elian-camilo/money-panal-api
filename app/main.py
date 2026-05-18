from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infraestructure.database import create_db_and_table
from app.presentation.api.v1.transaction_router import router as transaction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # I need the app create db and table since start.
    create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(transaction_router, prefix="/api/v1", tags=["transaction"])

@app.get("/")
def home() -> dict:
    return {"msg": "server is connect"}
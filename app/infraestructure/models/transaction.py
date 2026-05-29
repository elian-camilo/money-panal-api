from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime, UTC
from zoneinfo import ZoneInfo

def utc_now():
    return datetime.now(UTC)

# tz = ZoneInfo("America/Bogota")

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(SQLModel):
    amount: float = Field(ge=0, default=0.0)
    t_type: TransactionType = Field(default=TransactionType.EXPENSE) #"income" | "expense"
    description: str | None = Field(default=None, max_length=100)
    category_id: int | None = Field(default=None, foreign_key="categorytable.id")
    account_id: int | None = Field(default=None, foreign_key="accounttable.id")


class TransactionTable(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")
    created_at: datetime  = Field(default_factory=utc_now)


class TransactionPublic(TransactionBase):
    id: int
    user_id: int
    created_at: datetime


class TransactionCreate(TransactionBase):
    # or update
    pass
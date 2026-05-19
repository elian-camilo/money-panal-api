from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class TransactionBase(SQLModel):
    amount: float = Field(gt=0)
    t_type: TransactionType = Field(default=TransactionType.EXPENSE) #"income" | "expense"
    description: str | None = Field(default=None, max_length=100)
    caterogy_id: int | None = Field(default=None, foreign_key="categorytable.id")
    account_id: int | None = Field(default=None, foreign_key="accounttable.id")


class TransactionTable(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow)


class TransactionPublic(TransactionBase):
    id: int
    date: datetime


class TransactionCreate(TransactionBase):
    # or update
    pass
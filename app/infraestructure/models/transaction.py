from sqlmodel import SQLModel, Field
#from enum import Enum
from datetime import datetime


class TransactionBase(SQLModel):
    amount: float = Field(gt=0)
    t_type: str = Field(default="expense") #"income" | "expense"
    description: str
    date: datetime = Field(default_factory=datetime.utcnow)
    caterogy_id: int = Field(foreign_key="category.id")
    account_id: int = Field(foreign_key="account.id")


class TransactionTable(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TransactionPublic(TransactionBase):
    id: int


class TransactionCreate(TransactionBase):
    # or update
    pass
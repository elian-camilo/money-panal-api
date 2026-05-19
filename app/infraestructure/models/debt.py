from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date


class DebtType(str, Enum):
    LEND = "lend"
    BORROW = "borrow"


class DebtBase(SQLModel):
    person_name: str = Field(index=True, max_length=100)
    amount: float = Field(default=0.0)
    type: DebtType = Field(default=DebtType.LEND)
    due_date: date | None = Field(default=None)
    is_settled: bool = Field(default=False)


class DebtTable(DebtBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class DebtPublic(DebtBase):
    id: int


class DebtCreate(DebtBase):
    pass
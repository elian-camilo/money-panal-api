from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import date, datetime, UTC

def utc_now():
    return datetime.now(UTC)


class DebtType(str, Enum):
    LEND = "lend"
    BORROW = "borrow"


class DebtBase(SQLModel):
    person_name: str = Field(index=True, max_length=100)
    amount: float = Field(ge=0, default=0.0)
    type: DebtType = Field(default=DebtType.LEND)
    due_date: date | None = Field(default=None)
    is_settled: bool = Field(default=False)


class DebtTable(DebtBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")
    created_at: datetime = Field(default_factory=utc_now)


class DebtPublic(DebtBase):
    id: int
    user_id: int
    created_at: datetime


class DebtCreate(DebtBase):
    pass
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from enum import Enum

def utc_now():
    return datetime.now(UTC)


class Currency(str, Enum):
    COP = "cop"
    USD = "usd"
    CAD = "cad"
    CL = "cl"


class AccountBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    amount: float = Field(ge=0, default=0.0)
    profit_percentage: float = Field(ge=0.0,default=0.0)
    currency: Currency = Field(default=Currency.COP)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")


class AccountTable(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)


class AccountPublic(AccountBase):
    id: int
    created_at: datetime


class AccountCreate(AccountBase):
    pass
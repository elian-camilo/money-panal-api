from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class Currency(str, Enum):
    COP = "cop"
    USD = "usd"
    CAD = "cad"
    CL = "cl"


class AccountBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    amount: float = Field(default=0.0)
    profit_percentage: float = Field(default=0.0)
    currency: Currency = Field(default=Currency.COP)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")


class AccountTable(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AccountPublic(AccountBase):
    id: int
    created_at: datetime


class AccountCreate(AccountBase):
    pass
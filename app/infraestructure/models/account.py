from sqlmodel import SQLModel, Field
from enum import Enum

class Currency(str, Enum):
    COP = "cop"
    USD = "usd"
    CAD = "cad"
    CL = "cl"


class AccountBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    balance: float = Field(default=0.0)
    profit_percentage: float = Field(default=0.0)
    currency: Currency = Field(default=Currency.COP)


class AccountTable(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class AccountPublic(AccountBase):
    id: int


class AccountCreate(AccountBase):
    pass
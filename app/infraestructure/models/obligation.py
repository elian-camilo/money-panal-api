from sqlmodel import SQLModel, Field
from datetime import date, datetime, UTC

def utc_now():
    return datetime.now(UTC)


class ObligationBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    description: str | None = Field(default=None, max_length=100)
    amount: float = Field(ge=0, default=0.0)
    due_date: date | None = Field(default=None)
    is_paid: bool = Field(default=False)
    recurring: bool = Field(default=False)


class ObligationTable(ObligationBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")
    created_at: datetime = Field(default_factory=utc_now)


class ObligationPublic(ObligationBase):
    id: int
    user_id: int
    created_at: datetime


class ObligationCreate(ObligationBase):
    pass
from sqlmodel import SQLModel, Field
from datetime import date, datetime

class ObligationBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    description: str = Field(default=None, max_length=100)
    amount: float = Field(default=0.0)
    due_date: date | None = Field(default=None)
    is_paid: bool = Field(default=False)
    recurring: bool = Field(default=False)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")


class ObligationTable(ObligationBase, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ObligationPublic(ObligationBase):
    id: int
    created_at: datetime


class ObligationCreate(ObligationBase):
    pass
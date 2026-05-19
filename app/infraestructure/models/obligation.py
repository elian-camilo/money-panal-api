from sqlmodel import SQLModel, Field
from datetime import date

class ObligationBase(SQLModel):
    name: str = Field(index=True, max_length=30)
    description: str = Field(default=None, max_length=100)
    amount: float = Field(default=0.0)
    due_date: date | None = Field(default=None)
    is_paid: bool = Field(default=False)
    recurring: bool = Field(default=False)


class ObligationTable(ObligationBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ObligationPublic(ObligationBase):
    id: int


class ObligationCreate(ObligationBase):
    pass
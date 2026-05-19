from pydantic import BaseModel, ConfigDict
from datetime import date

class Obligation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    description: str | None = None
    amount: float
    due_date: date
    is_paid: bool
    recurring: bool
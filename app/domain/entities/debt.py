from pydantic import BaseModel, ConfigDict
from datetime import date

class Debt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    person_name: str
    amount: float
    type: str
    due_date: date | None = None
    is_settled: bool
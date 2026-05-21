from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class Debt(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    person_name: str
    amount: float
    type: str
    due_date: date | None = None
    is_settled: bool
    user_id: int | None = None
    created_at: datetime
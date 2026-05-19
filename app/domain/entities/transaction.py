from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    amount: float
    t_type: str
    description: str | None = None
    date: datetime
    caterogy_id: int | None = None
    account_id: int | None = None
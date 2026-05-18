from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    amount: float
    t_type: str
    description: str
    date: datetime
    caterogy_id: int
    account_id: int
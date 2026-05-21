from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    amount: float
    profit_percentage: float
    currency: str
    user_id: int | None = None
    created_at: datetime
from pydantic import BaseModel, ConfigDict

class Account(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    balance: float
    profit_percentage: float
    currency: str
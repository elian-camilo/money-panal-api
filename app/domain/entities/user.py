from pydantic import BaseModel, ConfigDict
from datetime import datetime

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    first_name: str
    last_name: str
    email: str
    password: str
    created_at: datetime | None = None
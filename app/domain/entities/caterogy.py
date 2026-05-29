from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    name: str
    description: str | None = None
    user_id: int | None = None
    created_at: datetime | None = None
    
from sqlmodel import SQLModel, Field
from datetime import datetime

class CaterogyBase(SQLModel):
    name: str = Field(max_length=30)
    description: str | None = Field(default=None, max_length=100)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")

class CategoryTable(CaterogyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CategoryPublic(CaterogyBase):
    id: int
    created_at: datetime

class CategoryCreate(CaterogyBase):
    pass
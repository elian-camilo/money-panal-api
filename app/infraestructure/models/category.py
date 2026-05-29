from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

def utc_now():
    return datetime.now(UTC)


class CaterogyBase(SQLModel):
    name: str = Field(max_length=30)
    description: str | None = Field(default=None, max_length=100)


class CategoryTable(CaterogyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="usertable.id")
    created_at: datetime = Field(default_factory=utc_now)


class CategoryPublic(CaterogyBase):
    id: int
    user_id: int
    created_at: datetime


class CategoryCreate(CaterogyBase):
    pass
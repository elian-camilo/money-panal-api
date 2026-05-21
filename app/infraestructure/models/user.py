from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

def utc_now():
    return datetime.now(UTC)


class UserBase(SQLModel):
    first_name: str = Field(index=True, max_length=30)
    last_name: str | None = Field(..., max_length=50)
    email: str = Field(..., index=True, max_length=80)
    hashed_password: str = Field(...,max_length=128)


class UserTable(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)


class UserPublic(UserBase):
    id: int
    created_at: datetime


class UserCreate(UserBase):
    pass
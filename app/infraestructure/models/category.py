from sqlmodel import SQLModel, Field

class CaterogyBase(SQLModel):
    name: str = Field(max_length=30)
    description: str | None = Field(default=None, max_length=100)


class CategoryTable(CaterogyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    pass

class CategoryPublic(CaterogyBase):
    id: int

class CategoryCreate(CaterogyBase):
    pass
from sqlmodel import Session, select
from app.domain.repositories.category_repository import CategoryRespositoryInterface
from app.domain.entities.caterogy import Category as CategoryEntity
from ..models.category import CategoryTable


class SQLModelCategoryRespository(CategoryRespositoryInterface):
    def __init__(self, session: Session):
        self.session = session

    def save(self, category: CategoryEntity) -> CategoryEntity:
        category_db = CategoryTable.model_validate(category)

        self.session.add(category_db)
        self.session.flush()
        self.session.refresh(category_db)

        return CategoryEntity.model_validate(category_db)
    
    def get_all(self, offset: int, limit: int) -> list[CategoryEntity]:
        category_db = self.session.exec(select(CategoryTable).offset(offset).limit(limit)).all()
        return [CategoryEntity.model_validate(category) for category in category_db]
    
    def get_by_id(self, id: int):
        category_db = self.session.get(CategoryTable, id)
        if not category_db:
            return None
        return CategoryEntity.model_validate(category_db)

    def update(self, id: int, category: CategoryEntity) -> CategoryEntity:
        category_db = self.session.get(CategoryTable, id)
        if not category_db:
            return None
        category_data = category.model_dump()
        category_db.sqlmodel_update(category_db)

        self.session.add(category_db)
        self.session.flush()
        self.session.refresh(category_db)

        return CategoryEntity.model_validate(category_db)
    
    def delete(self, id: int) -> bool:
        category_db = self.session.get(CategoryTable, id)
        if not category_db:
            return None
        self.session.delete(category_db)
        self.session.flush()

        return True
from fastapi import APIRouter, Depends
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.category_service import (
    CreateCategoryUseCase,
    ListCategoryUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from app.infraestructure.database import get_session
from app.domain.entities.caterogy import Category
from app.infraestructure.models.category import (
    CategoryPublic,
    CategoryCreate
)
from app.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/categories", dependencies=[Depends(get_current_user)])

@router.post("/", response_model=CategoryPublic)
def create_category(category: CategoryCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = CreateCategoryUseCase(uow=uow)
    domain_category = Category.model_validate({
        **category.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(domain_category, user_id=current_user.id)
    
@router.get("/", response_model=list[CategoryPublic])
def get_all_category(offset: int = 0, limit: int = 10, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = ListCategoryUseCase(uow=uow)
    return service.execute(offset, limit, current_user=current_user)
    
@router.get("/{id}", response_model=CategoryPublic)
def get_category(id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = GetCategoryUseCase(uow=uow)
    return service.execute(id, current_user=current_user)
    
@router.put("/{id}", response_model=CategoryPublic)
def update_category(id: int, category: CategoryCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = UpdateCategoryUseCase(uow=uow)
    domain_category = Category.model_validate({
        **category.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(id, domain_category, current_user=current_user)
    
@router.delete("/{id}")
def delete_category(id: int, session=Depends(get_session), current_user=Depends(get_current_user)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteCategoryUseCase(uow=uow)
    service.execute(id, current_user=current_user)
    return {"status": "success", "message": "Category deleted successfully", "delete_id": id}
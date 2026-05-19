from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.category_service import (
    CreateCategoryUseCase,
    ListCategoryUseCase,
    GetCategoryUseCase,
    UpdateCategoryUseCase,
    DeleteCategoryUseCase
)
from app.infraestructure.database import get_session
from app.infraestructure.models.category import (
    CategoryPublic,
    CategoryCreate
)

router = APIRouter(prefix="/category")

@router.post("/", response_model=CategoryPublic)
def create_category(category: CategoryCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = CreateCategoryUseCase(uow=uow)

    try:
        with uow:
            return service.execute(category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[CategoryPublic])
def get_all_category(offset: int = 0, limit: int = 10, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListCategoryUseCase(uow=uow)

    try:
        with uow:
            return service.execute(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}", response_model=CategoryPublic)
def get_category(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetCategoryUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}", response_model=CategoryPublic)
def update_category(id: int, category: CategoryCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateCategoryUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id, category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_category(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteCategoryUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
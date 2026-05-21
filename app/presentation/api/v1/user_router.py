from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.user_service import (
    CreateUserUseCase,
    ListUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase
)
from app.infraestructure.database import get_session
from app.infraestructure.models.user import (
    UserPublic,
    UserCreate
)

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = CreateUserUseCase(uow=uow)

    try:
        with uow:
            return service.execute(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[UserPublic])
def get_all_users(offset: int = 0, limit: int = 10, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListUserUseCase(uow=uow)

    try:
        with uow:
            return service.execute(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}", response_model=UserPublic)
def get_user(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetUserUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}", response_model=UserPublic)
def update_user(id: int, user: UserCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateUserUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_user(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteUserUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
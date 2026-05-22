from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.account_service import (
    CreateAccountUseCase,
    ListAccountUseCase,
    GetAccountUseCase,
    UpdateAccountUseCase,
    DeleteAccountUseCase
)
from app.infraestructure.database import get_session
from app.infraestructure.models.account import (
    AccountPublic,
    AccountCreate
)
from app.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/accounts", dependencies=[Depends(get_current_user)])

@router.post("/", response_model=AccountPublic)
def create_account(account: AccountCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = CreateAccountUseCase(uow=uow)

    try:
        with uow:
            return service.execute(account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[AccountPublic])
def get_all_accounts(offset: int = 0, limit: int = 10, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListAccountUseCase(uow=uow)

    try:
        with uow:
            return service.execute(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}", response_model=AccountPublic)
def get_account(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetAccountUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}", response_model=AccountPublic)
def update_account(id: int, account: AccountCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateAccountUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id, account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_account(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteAccountUseCase(uow=uow)

    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
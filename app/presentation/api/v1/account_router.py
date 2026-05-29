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
from app.domain.entities.account import Account
from app.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/accounts", dependencies=[Depends(get_current_user)])


@router.post("/", response_model=AccountPublic)
def create_account(account: AccountCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = CreateAccountUseCase(uow=uow)
    domain_account = Account.model_validate({
        **account.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(domain_account, user_id=current_user.id)


@router.get("/", response_model=list[AccountPublic])
def get_all_accounts(offset: int = 0, limit: int = 10, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = ListAccountUseCase(uow=uow)
    return service.execute(offset, limit, current_user=current_user)
    

@router.get("/{id}", response_model=AccountPublic)
def get_account(id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = GetAccountUseCase(uow=uow)
    return service.execute(id, current_user=current_user)
    

@router.put("/{id}", response_model=AccountPublic)
def update_account(id: int, account: AccountCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = UpdateAccountUseCase(uow=uow)
    domain_account = Account.model_validate({
        **account.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(id, domain_account, current_user=current_user)
    

@router.delete("/{id}")
def delete_account(id: int, session=Depends(get_session), current_user=Depends(get_current_user)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteAccountUseCase(uow=uow)
    service.execute(id, current_user=current_user)
    return {"status": "success", "message": "Account deleted successfully", "deleted_id": id}
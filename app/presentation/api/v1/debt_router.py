from fastapi import APIRouter, Depends
from app.domain.entities.user import User
from app.domain.entities.debt import Debt
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.debt_service import (
    CreateDebtUseCase,
    ListDebtUseCase,
    GetDebtUseCase,
    UpdateDebtUseCase,
    DeleteDebtUseCase
)
from app.infraestructure.database import get_session
from app.infraestructure.models.debt import (
    DebtPublic,
    DebtCreate
)
from app.presentation.api.dependencies import get_current_user

router = APIRouter(prefix="/debts", dependencies=[Depends(get_current_user)])


@router.post("/", response_model=DebtPublic)
def create_debt(
    debt: DebtCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = CreateDebtUseCase(uow=uow)
    domain_debt = Debt.model_validate({
        **debt.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(domain_debt)


@router.get("/", response_model=list[DebtPublic])
def get_all_debts(
    offset: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = ListDebtUseCase(uow=uow)
    return service.execute(offset, limit, current_user)


@router.get("/{id}", response_model=DebtPublic)
def get_debt(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = GetDebtUseCase(uow=uow)
    return service.execute(id, current_user)


@router.put("/{id}", response_model=DebtPublic)
def update_debt(
    id: int,
    debt: DebtCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = UpdateDebtUseCase(uow=uow)
    domain_debt = Debt.model_validate({
        **debt.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(id, domain_debt, current_user)


@router.delete("/{id}")
def delete_debt(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> dict:
    uow = UnitOfWork(session)
    service = DeleteDebtUseCase(uow=uow)
    service.execute(id, current_user)
    return {"status": "success", "message": "Debt deleted successfully", "delete_id": id}

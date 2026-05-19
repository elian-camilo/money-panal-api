from fastapi import APIRouter, Depends, HTTPException
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

router = APIRouter(prefix="/debts")

@router.post("/", response_model=DebtPublic)
def create_debt(debt: DebtCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = CreateDebtUseCase(uow=uow)
    try:
        with uow:
            return service.execute(debt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[DebtPublic])
def get_all_debts(offset: int = 0, limit: int = 10, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListDebtUseCase(uow=uow)
    try:
        with uow:
            return service.execute(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}", response_model=DebtPublic)
def get_debt(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetDebtUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}", response_model=DebtPublic)
def update_debt(id: int, debt: DebtCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateDebtUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id, debt)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_debt(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteDebtUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

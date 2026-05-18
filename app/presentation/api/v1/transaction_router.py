from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.domain.entities.transaction import Transaction
from app.application.services.transaction_service import CreateTransactionUseCase, GetTransactionUseCase, ListTransactionUseCase, UpdateTransactionUseCase, DeleteTransactionUseCase
from app.infraestructure.database import get_session
from app.infraestructure.models.transaction import TransactionPublic, TransactionCreate

router = APIRouter(prefix="/transactions")

@router.post("/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionCreate, session=Depends(get_session)):
    # Instance of our infra SQLModel through a UOW
    uow = UnitOfWork(session)

    # Pass it an implementation of our rules
    service = CreateTransactionUseCase(uow=uow)

    # Execute and traslate errors
    try:
        with uow:
            return service.execute(transaction)
    except ValueError as e:
        # The ouw all ready made 'rollback' cause detect and exception into 'with'
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[TransactionPublic])
def get_all_transactions(offset: int = 0, limit: int = 100, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListTransactionUseCase(uow=uow)
    try:
        with uow:
            return service.execute(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}", response_model=TransactionPublic)
def get_transaction(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetTransactionUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}", response_model=TransactionPublic)
def update_transaction(id: int, transaction: TransactionCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateTransactionUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id, transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_trasaction(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteTransactionUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
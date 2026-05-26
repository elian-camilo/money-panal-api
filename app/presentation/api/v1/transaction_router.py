from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.transaction_service import CreateTransactionUseCase, GetTransactionUseCase, ListTransactionUseCase, UpdateTransactionUseCase, DeleteTransactionUseCase
from app.infraestructure.database import get_session
from app.presentation.api.dependencies import get_current_user
from app.infraestructure.models.transaction import TransactionPublic, TransactionCreate

router = APIRouter(prefix="/transactions", dependencies=[Depends(get_current_user)])

@router.post("/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionCreate, session=Depends(get_session)):
    # Instance of our infra SQLModel through a UOW
    uow = UnitOfWork(session)
    # Pass it an implementation of our rules
    service = CreateTransactionUseCase(uow=uow)
    # Execute
    return service.execute(transaction)
    
@router.get("/", response_model=list[TransactionPublic])
def get_all_transactions(offset: int = 0, limit: int = 100, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListTransactionUseCase(uow=uow)
    return service.execute(offset, limit)
    
@router.get("/{id}", response_model=TransactionPublic)
def get_transaction(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetTransactionUseCase(uow=uow)
    return service.execute(id)
    
@router.put("/{id}", response_model=TransactionPublic)
def update_transaction(id: int, transaction: TransactionCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateTransactionUseCase(uow=uow)
    return service.execute(id, transaction)

    
@router.delete("/{id}")
def delete_trasaction(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteTransactionUseCase(uow=uow)
    service.execute(id)
    return {"status": "success", "message": "Transaction deleted successfully", "delete_id": id}
from fastapi import APIRouter, Depends
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.transaction_service import CreateTransactionUseCase, GetTransactionUseCase, ListTransactionUseCase, UpdateTransactionUseCase, DeleteTransactionUseCase
from app.infraestructure.database import get_session
from app.presentation.api.dependencies import get_current_user
from app.infraestructure.models.transaction import TransactionPublic, TransactionCreate
from app.domain.entities.transaction import Transaction

router = APIRouter(prefix="/transactions", dependencies=[Depends(get_current_user)])


@router.post("/", response_model=TransactionPublic)
def create_transaction(transaction: TransactionCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = CreateTransactionUseCase(uow=uow)

    # Map to Domain Entity using model_validate and dict unpacking
    domain_transaction = Transaction.model_validate({
        **transaction.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(domain_transaction, user_id=current_user.id)

@router.get("/", response_model=list[TransactionPublic])
def get_all_transactions(offset: int = 0, limit: int = 100, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = ListTransactionUseCase(uow=uow)
    return service.execute(offset, limit, current_user=current_user)
    
@router.get("/{id}", response_model=TransactionPublic)
def get_transaction(id: int, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = GetTransactionUseCase(uow=uow)
    return service.execute(id, current_user=current_user)
    
@router.put("/{id}", response_model=TransactionPublic)
def update_transaction(id: int, transaction: TransactionCreate, session=Depends(get_session), current_user=Depends(get_current_user)):
    uow = UnitOfWork(session)
    service = UpdateTransactionUseCase(uow=uow)
    # Map to Domain Entity using model_validate and dict unpacking
    domain_transaction = Transaction.model_validate({
        **transaction.model_dump(), 
        "user_id": current_user.id
    })
    return service.execute(id, domain_transaction, current_user=current_user)

    
@router.delete("/{id}")
def delete_trasaction(id: int, session=Depends(get_session), current_user = Depends(get_current_user)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteTransactionUseCase(uow=uow)
    service.execute(id, current_user=current_user)
    return {"status": "success", "message": "Transaction deleted successfully", "delete_id": id}
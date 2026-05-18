from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.domain.entities.transaction import Transaction
from app.application.services.transaction_service import CreateTransactionUseCase
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
    

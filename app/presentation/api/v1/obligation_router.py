from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.obligation_service import CreateObligationUseCase, GetObligationUseCase, ListObligationUseCase, UpdateObligationUseCase, DeleteObligationUseCase
from app.infraestructure.database import get_session
from app.presentation.api.dependencies import get_current_user
from app.infraestructure.models.obligation import ObligationPublic, ObligationCreate

router = APIRouter(prefix="/obligations", dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ObligationPublic)
def create_obligation(obligation: ObligationCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = CreateObligationUseCase(uow=uow)
    return service.execute(obligation)
    
@router.get("/", response_model=list[ObligationPublic])
def get_all_obligations(offset: int = 0, limit: int = 100, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListObligationUseCase(uow=uow)
    return service.execute(offset, limit)
    
@router.get("/{id}", response_model=ObligationPublic)
def get_obligation(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetObligationUseCase(uow=uow)
    return service.execute(id)
    
@router.put("/{id}", response_model=ObligationPublic)
def update_obligation(id: int, obligation: ObligationCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateObligationUseCase(uow=uow)
    return service.execute(id, obligation)
    
@router.delete("/{id}")
def delete_obligation(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteObligationUseCase(uow=uow)
    service.execute(id)
    return {"status": "success", "message": "Obligation deleted successfully", "delete_id": id}
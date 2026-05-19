from fastapi import APIRouter, Depends, HTTPException
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.obligation_service import CreateObligationUseCase, GetObligationUseCase, ListObligationUseCase, UpdateObligationUseCase, DeleteObligationUseCase
from app.infraestructure.database import get_session
from app.infraestructure.models.obligation import ObligationPublic, ObligationCreate

router = APIRouter(prefix="/obligations")

@router.post("/", response_model=ObligationPublic)
def create_obligation(obligation: ObligationCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = CreateObligationUseCase(uow=uow)
    try:
        with uow:
            return service.execute(obligation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[ObligationPublic])
def get_all_obligations(offset: int = 0, limit: int = 100, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = ListObligationUseCase(uow=uow)
    try:
        with uow:
            return service.execute(offset, limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}", response_model=ObligationPublic)
def get_obligation(id: int, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = GetObligationUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.put("/{id}", response_model=ObligationPublic)
def update_obligation(id: int, obligation: ObligationCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = UpdateObligationUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id, obligation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/{id}")
def delete_obligation(id: int, session=Depends(get_session)) -> dict:
    uow = UnitOfWork(session)
    service = DeleteObligationUseCase(uow=uow)
    try:
        with uow:
            return service.execute(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
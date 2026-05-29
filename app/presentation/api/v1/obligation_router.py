from fastapi import APIRouter, Depends
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.obligation_service import (
    CreateObligationUseCase,
    GetObligationUseCase,
    ListObligationUseCase,
    UpdateObligationUseCase,
    DeleteObligationUseCase
)
from app.domain.entities.obligation import Obligation
from app.domain.entities.user import User
from app.infraestructure.database import get_session
from app.presentation.api.dependencies import get_current_user
from app.infraestructure.models.obligation import ObligationPublic, ObligationCreate

router = APIRouter(prefix="/obligations", dependencies=[Depends(get_current_user)])


@router.post("/", response_model=ObligationPublic)
def create_obligation(
    obligation: ObligationCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = CreateObligationUseCase(uow=uow)
    obligation_entity = Obligation.model_validate({
        **obligation.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(obligation_entity)


@router.get("/", response_model=list[ObligationPublic])
def get_all_obligations(
    offset: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = ListObligationUseCase(uow=uow)
    return service.execute(offset, limit, current_user)


@router.get("/{id}", response_model=ObligationPublic)
def get_obligation(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = GetObligationUseCase(uow=uow)
    return service.execute(id, current_user)


@router.put("/{id}", response_model=ObligationPublic)
def update_obligation(
    id: int,
    obligation: ObligationCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = UpdateObligationUseCase(uow=uow)
    obligation_entity = Obligation.model_validate({
        **obligation.model_dump(),
        "user_id": current_user.id
    })
    return service.execute(id, obligation_entity, current_user)


@router.delete("/{id}")
def delete_obligation(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> dict:
    uow = UnitOfWork(session)
    service = DeleteObligationUseCase(uow=uow)
    service.execute(id, current_user)
    return {"status": "success", "message": "Obligation deleted successfully", "deleted_id": id}
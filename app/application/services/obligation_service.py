from app.application.interfaces.unit_of_work import IUnitOfWork
from app.domain.entities.obligation import Obligation
from app.domain.entities.user import User
from datetime import date
from app.domain.exceptions import (
    ResourceNotFoundException,
    UnprocessableEntityException,
    UnauthorizedException
)
from app.core.logger import get_logger

logger = get_logger(__name__)


class CreateObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, obligation: Obligation) -> Obligation:
        # Business Rules
        if obligation.due_date < date.today():
            logger.warning("invalid_due_date", due_date=obligation.due_date)
            raise UnprocessableEntityException("The due date don't be less than today.")
        with self.uow:
            obligation_saved = self.uow.obligation_repository.save(obligation)
            
        logger.info("obligation_created", id=obligation_saved.id, amount=obligation_saved.amount, due_date=obligation_saved.due_date, user_id=obligation_saved.user_id)
        return obligation_saved


class ListObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, offset: int, limit: int, current_user: User) -> list[Obligation]:
        with self.uow:
            obligations_list = self.uow.obligation_repository.get_all(offset, limit, user_id=current_user.id)
            
        logger.debug("obligations_listed", offset=offset, limit=limit, user_id=current_user.id)
        return obligations_list


class GetObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> Obligation:
        with self.uow:
            obligation = self.uow.obligation_repository.get_by_id(id)
            if not obligation:
                logger.warning("obligation_not_found", id=id)
                raise ResourceNotFoundException(f"Obligation ID:{id} doesn't exist.")
            if obligation.user_id != current_user.id:
                logger.warning("obligation_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Obligation ID:{id}.")

        logger.debug("obligation_retrieved", id=obligation.id, amount=obligation.amount, due_date=obligation.due_date, user_id=obligation.user_id)
        return obligation
    

class UpdateObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, obligation: Obligation, current_user: User) -> Obligation:
        # Business Rules
        if obligation.due_date < date.today():
            logger.warning("invalid_due_date", due_date=obligation.due_date)
            raise UnprocessableEntityException("The due date don't be less than today.")

        with self.uow:
            obligation_db = self.uow.obligation_repository.get_by_id(id)
            if not obligation_db:
                logger.warning("obligation_not_found", id=id)
                raise ResourceNotFoundException(f"Obligation ID:{id} doesn't exist.")
            if obligation_db.user_id != current_user.id:
                logger.warning("obligation_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Obligation ID:{id}.")

            obligation_updated = self.uow.obligation_repository.update(id, obligation)

        logger.info("obligation_updated", id=obligation_updated.id, amount=obligation_updated.amount, due_date=obligation_updated.due_date, user_id=obligation_updated.user_id)
        return obligation_updated
    

class DeleteObligationUseCase:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    def execute(self, id: int, current_user: User) -> None:
        with self.uow:
            obligation_db = self.uow.obligation_repository.get_by_id(id)
            if not obligation_db:
                logger.warning("obligation_not_found", id=id)
                raise ResourceNotFoundException(f"Obligation ID:{id} doesn't exist.")
            if obligation_db.user_id != current_user.id:
                logger.warning("obligation_access_denied", id=id, user_id=current_user.id)
                raise UnauthorizedException(f"Access denied for Obligation ID:{id}.")

            self.uow.obligation_repository.delete(id)
            
        logger.info("obligation_deleted", id=id)
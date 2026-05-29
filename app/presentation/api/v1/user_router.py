from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from app.infraestructure.unit_of_work import UnitOfWork
from app.application.services.user_service import (
    RegisterUserUseCase,
    RegisterUserCommand,
    ListUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    AuthenticateUserUseCase,
    LoginUserCommand
)
from app.infraestructure.database import get_session
from app.infraestructure.models.user import (
    UserPublic,
    UserCreate
)
from app.infraestructure.security.password_hasher import PasswordHasher
from app.infraestructure.security.jwt_provider import JwtTokenProvider
from app.presentation.api.dependencies import get_current_user
from app.domain.entities.user import User

router = APIRouter(prefix="/users")

hasher = PasswordHasher()
jwt_provider = JwtTokenProvider()

templates = Jinja2Templates(directory="app/presentation/web/templates")
router.mount("/static", StaticFiles(directory="app/presentation/web/static"), name="static")

### Pages ###

@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

### Endpoints ###

@router.post("/login", tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = AuthenticateUserUseCase(uow=uow, hasher=hasher, token_provider=jwt_provider)
    
    command = LoginUserCommand(
        email=form_data.username,
        password=form_data.password
    )
    token = service.execute(command)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/", response_model=UserPublic, tags=["auth"])
def register_user(user: UserCreate, session=Depends(get_session)):
    uow = UnitOfWork(session)
    service = RegisterUserUseCase(uow=uow, hasher=hasher)
    
    command = RegisterUserCommand(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    return service.execute(command)


@router.get("/", response_model=list[UserPublic])
def get_all_users(
    offset: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = ListUserUseCase(uow=uow)
    return service.execute(offset, limit, current_user)


@router.get("/{id}", response_model=UserPublic)
def get_user(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = GetUserUseCase(uow=uow)
    return service.execute(id, current_user)


@router.put("/{id}", response_model=UserPublic)
def update_user(
    id: int,
    user: UserCreate,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):
    uow = UnitOfWork(session)
    service = UpdateUserUseCase(uow=uow)
    return service.execute(id, user, current_user)


@router.delete("/{id}")
def delete_user(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> dict:
    uow = UnitOfWork(session)
    service = DeleteUserUseCase(uow=uow)
    service.execute(id, current_user)
    return {"status": "success", "message": "User deleted successfully", "deleted_id": id}
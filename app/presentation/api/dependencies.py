from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.infraestructure.database import get_session
from app.infraestructure.unit_of_work import UnitOfWork
from app.infraestructure.security.jwt_provider import JwtTokenProvider
from app.domain.entities.user import User
from fastapi import Request

# Configuramos el esquema acá centralizado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")
jwt_provider = JwtTokenProvider()

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Verificar y decodificar el token usando nuestra infraestructura
    payload = jwt_provider.verify_token(token)
    if not payload:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    # 2. Buscar al usuario en la base de datos
    uow = UnitOfWork(session)
    with uow:
        user = uow.user_repository.get_by_email(email)
        if user is None:
            raise credentials_exception
            
        return user

def get_current_user_from_cookie(
    request: Request,
    session = Depends(get_session)
) -> User | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
        
    # 1. Verificar y decodificar el token
    payload = jwt_provider.verify_token(token)
    if not payload:
        return None
        
    email: str = payload.get("sub")
    if not email:
        return None

    # 2. Buscar al usuario en la base de datos
    uow = UnitOfWork(session)
    with uow:
        user = uow.user_repository.get_by_email(email)
        return user
import pytest
from unittest.mock import MagicMock

from app.application.services.user_service import AuthenticateUserUseCase, LoginUserCommand
from app.domain.entities.user import User
from app.domain.exceptions import UnauthorizedException

def test_authenticate_user_success():
    # 1. Creamos los mocks de las interfaces que necesita la construcción del user_service.
    uow = MagicMock()
    hasher = MagicMock()
    token_provider = MagicMock()

    # creamos un usuario mock que sera el resultado mock de .get_by_email
    fake_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="hashed_password_123"
    )
    # establecemos que cuando se llame a la función .get_by_email el resultado sea el objeto *fake_user*
    uow.user_repository.get_by_email.return_value = fake_user

    # establecemos que cuando se llame a la función verify_password el resultado sea *True*
    hasher.verify_password.return_value = True

    # establecemos que cuando se llame a la función verify_password el resultado sea *fake-jwt-token*
    token_provider.generate_token.return_value = "fake-jwt-token"

    # instanciamos el caso de uso inyectandole las interfaces mockeadas. **AuthenticateUserUseCase**.
    user_case = AuthenticateUserUseCase(
        uow=uow,
        hasher=hasher,
        token_provider=token_provider
    )

    # Ejecutamos el caso de uso pasandole las credenciales mediante un *command*.
    # Realmente no importa la password ya que tenemos seteado que verify_password es True.
    command= LoginUserCommand(email="leo@messi.com", password="password_correcto")
    token = user_case.execute(command)

    # Assert (verificar que la logica de negocio se cumplio).
    # El servicio retorna el token que seteamos antes *fake-jwt-token*
    assert token == "fake-jwt-token"

    # Ademas de verificar la respuesta, verificamos también el comportamiento.
    ## verificamos que esta función fue llamada y que el parametro usado fue "leo@messi.com" 
    uow.user_repository.get_by_email.assert_called_once_with("leo@messi.com")
    ## verificamos que esta función fue llamada y que los parametros usados fueros especificamente "password_correcto" y "hashed_password_123" 
    hasher.verify_password.assert_called_once_with("password_correcto", "hashed_password_123")
    ## verificamos que esta función fue llamada, sin importar con que parametro. 
    token_provider.generate_token.assert_called_once()
	## verificamos que esta función fue llamada y que el parametro usado fue "{"sub": "leo@messi.com"}".
    token_provider.generate_token.assert_called_once_with({"sub": "leo@messi.com"})
    

def test_authenticate_user_wrong_password():
    uow = MagicMock()
    hasher = MagicMock()
    token_provider = MagicMock()

    fake_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="hashed_password_123"
    )
    uow.user_repository.get_by_email.return_value = fake_user

    # False
    hasher.verify_password.return_value = False

    use_case = AuthenticateUserUseCase(
        uow=uow,
        hasher=hasher,
        token_provider=token_provider
    )

    command = LoginUserCommand(
        email="leo@messi.com",
        password="password_incorrecto"
    )

    # le decimos a Pytest que esperamos que esta ejecución lance una excepción especifica.
    with pytest.raises(UnauthorizedException) as exc_info:
        use_case.execute(command)

    # verificamos mensaje esperado
    assert str(exc_info.value) == "Email or password incorrect."

    # Verificamos que nunca se ejecute la función que provee el token.
    token_provider.generate_token.assert_not_called()


def test_authenticate_user_not_found():
    uow = MagicMock()
    hasher = MagicMock()
    token_provider = MagicMock()

    uow.user_repository.get_by_email.return_value = None

    user_case = AuthenticateUserUseCase(
        uow=uow,
        hasher=hasher,
        token_provider=token_provider
    )

    command = LoginUserCommand(
        email="leo@ronaldo.com", 
        password="password_correcto"
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        user_case.execute(command)
    
    assert str(exc_info.value) == "Email or password incorrect."

    hasher.verify_password.assert_not_called()
    token_provider.generate_token.assert_not_called()

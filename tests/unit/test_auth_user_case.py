import pytest
from unittest.mock import MagicMock

from app.application.services.user_service import AuthenticateUserUseCase, LoginUserCommand
from app.domain.entities.user import User
from app.domain.exceptions import UnauthorizedException

def test_authenticate_user_success():
    # 1. Created mock from interfaces.
    uow = MagicMock()
    hasher = MagicMock()
    token_provider = MagicMock()

    # simulamos el comportamiento de resostirio de user self.uow.user_repository.
    # cuando el caso de uso llame uow.user_repository.get_by_email regresamos un usuario en memoria.
    fake_user = User(
        id=1,
        first_name="Leo",
        last_name="Messi",
        email="leo@messi.com",
        password="hashed_password_123"
    )
    # significa que cuando el servicio haga el .get_by_email va a regresar
    # auntomaticamente el fake_user? En vez de consultar realmente el repo?
    uow.user_repository.get_by_email.return_value = fake_user

    # el mock me permite establecer la respuesta para una función antes que la tome?
    # para que no la ejecute si no que directamente se setee el valor que estoy escribiendo aquí?
    # simulamos el hasher
    hasher.verify_password.return_value = True

    # Cuando vaya a realizar esta acción realmente retorna este valor dirctamente.
    # Simulación del token provider
    token_provider.generate_token.return_value = "fake-jwt-token"

    # instanciamos el caso de uso inyectandole los mocks
    # instanciarlo como lo hacemos en el router.
    user_case = AuthenticateUserUseCase(
        uow=uow,
        hasher=hasher,
        token_provider=token_provider
    )

    # Ejecutamos el caso de uso pasandole las credenciales por medio del command.
    # realmente no importa la password ya que tenemos seteado que verify_password es True.
    command= LoginUserCommand(email="leo@messi.com", password="password_correcto")
    token = user_case.execute(command)

    # Assert (verificar que la logica de negocio se cumplio).
    # el servicio retorna un token, ese token lo mockeamos antes.
    assert token == "fake-jwt-token"

    # Verificamos el comportamiento, esto no lo entiendo bien.
    uow.user_repository.get_by_email.assert_called_once_with("leo@messi.com")
    hasher.verify_password.assert_called_once_with("password_correcto", "hashed_password_123")
    # assert_called_once() solo verifica que la funcion haya sido llamada una vez sin importar los argumentos.
    token_provider.generate_token.assert_called_once()
    # para validar que se ejecuto con los argumentos correctos usamos assert_called_once_with().
    # pasamos el payload que se espera recibir.
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

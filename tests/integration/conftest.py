import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool

from app.main import app
from app.infraestructure.models.user import UserTable
from app.infraestructure.models.category import CategoryTable
from app.infraestructure.models.account import AccountTable
from app.domain.entities.user import User
from app.infraestructure.database import get_session
from app.presentation.api.dependencies import get_current_user

# 1. Create engine to database in memory from tests
DATABASE_URL = "postgresql://tester:test123@localhost:5433/testing_db"

engine = create_engine(
    DATABASE_URL, 
    echo=False,
)

# 2. override session inyect depends
def override_get_session():
    with Session(engine) as session:
        yield session

def override_get_current_user():
    # Retornamos un usuario falso/mockeado para saltar la auth en los tests
    return User(id=1, first_name="Test", last_name="User", email="test@test.com", password="testing_password")

# 3. apply override session and auth
app.dependency_overrides[get_session] = override_get_session

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="session", name="client")
def client_fixture():
    return TestClient(app)

@pytest.fixture(name="session")
def session_fixture():
    with Session(engine) as session:
        yield session

@pytest.fixture(name="seed_db")
def seed_db_fixture(session: Session):
    # 1. Crear Usuario
    user = UserTable(
        id=1, 
        first_name="Test", 
        last_name="User", 
        email="test@test.com", 
        password="hash"
    )
    session.add(user)
    session.commit()
    
    # 2. Crear Cuenta
    account = AccountTable(
        id=1, 
        name="Test Account", 
        amount=100000.0, 
        profit_percentage=0.0, 
        currency="cop", 
        user_id=1
    )
    # 3. Crear Categoría
    category = CategoryTable(
        id=1, 
        name="Test Category", 
        description="Test Description", 
        user_id=1
    )
    
    session.add(account)
    session.add(category)
    session.commit()

@pytest.fixture(autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)
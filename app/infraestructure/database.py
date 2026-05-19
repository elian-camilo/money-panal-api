from sqlmodel import Session, SQLModel, create_engine
# import all models we have.
from .models.transaction import TransactionTable
from .models.category import CategoryTable
from .models.account import AccountTable
from .models.obligation import ObligationTable
from .models.debt import DebtTable

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
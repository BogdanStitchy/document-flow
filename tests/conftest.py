import pytest
from sqlalchemy import create_engine

from src.db.models import base
from src.db.database_setup import set_new_engine

data_base_local = "sqlite:///B:/работа/проекты с работы/document_flow/tests/testDB.db"
data_base_memory = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def create_database():
    engine = create_engine(data_base_local)
    base.Base.metadata.drop_all(bind=engine)
    base.Base.metadata.create_all(engine)
    set_new_engine(engine)

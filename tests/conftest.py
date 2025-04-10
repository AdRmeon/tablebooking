import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.main import app
from app.core.database import get_session
from app.core.config import get_settings
from app.core.logger import logger


settings = get_settings()
logger.setLevel(logging.CRITICAL)


def create_test_database():
    db_name = f"{settings.POSTGRES_DB}_test"
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    host = settings.DB_HOST
    port = int(settings.DB_PORT)

    con = psycopg2.connect(
        dbname="postgres", user=user, password=password, host=host, port=port
    )
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = con.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    con.close()


@pytest.fixture(scope="session")
def test_engine():
    create_test_database()
    engine = create_engine(settings.database_test_url)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture()
def clean_db(test_engine):
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)


@pytest.fixture(name="session")
def session_fixture(test_engine):
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

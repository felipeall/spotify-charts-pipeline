import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import scoped_session, sessionmaker

from src.models.base import Base


@pytest.fixture(scope="session")
def connection():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("TEST_POSTGRES_USER"),
        password=os.getenv("TEST_POSTGRES_PASSWORD"),
        host=os.getenv("TEST_POSTGRES_HOST"),
        database=os.getenv("TEST_POSTGRES_DB"),
    )
    engine = create_engine(url)
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=connection))
    transaction.rollback()

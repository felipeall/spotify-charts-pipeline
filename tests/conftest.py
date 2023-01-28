import os
import random
import uuid
from datetime import date

import pytest
from sqlalchemy import create_engine, func, select
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


@pytest.fixture
def get_random_int() -> int:
    return random.randint(1, 100)


@pytest.fixture
def get_random_string() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def get_today_date() -> date:
    return date.today()


@pytest.fixture
def count_records_table(db_session):
    def _execute(table):
        result = db_session.execute(select(func.count()).select_from(table))
        return result.scalars().one()

    return _execute

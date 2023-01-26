import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import scoped_session, sessionmaker

import src.models.base
from src.models.user import User


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


def seed_database():
    users = [
        {
            "id": 1,
            "name": "John Doe",
        },
        # ...
    ]

    for user in users:
        db_user = User(**user)
        db_session.add(db_user)
    db_session.commit()


@pytest.fixture(scope="session")
def setup_database(connection):
    src.models.base.Base.metadata.bind = connection
    src.models.base.Base.metadata.create_all()

    # seed_database()

    yield

    src.models.base.Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()

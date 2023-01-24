import os
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()


@dataclass
class PostgresClient:
    username: str = os.getenv("POSTGRES_USER")
    password: str = os.getenv("POSTGRES_PASSWORD")
    hostname: str = os.getenv("POSTGRES_HOST")
    port: str = os.getenv("POSTGRES_PORT")
    database: str = os.getenv("POSTGRES_DB")

    def __post_init__(self) -> None:
        engine: Engine = create_engine(
            f"postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}"
        )
        session_maker: sessionmaker = sessionmaker(bind=engine)
        self.session: Session = session_maker()

from src.clients.postgres import PostgresClient
from src.models import Base

if __name__ == "__main__":
    Base.metadata.bind = PostgresClient().session.bind
    Base.metadata.create_all()

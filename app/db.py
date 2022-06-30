import os
from sqlmodel import Session, create_engine, SQLModel


USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
postgres_url = f"postgresql://{USER}:{PASSWORD}@db"

print(f"\n user => {USER}\n password => {PASSWORD}\n")


engine = create_engine(postgres_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

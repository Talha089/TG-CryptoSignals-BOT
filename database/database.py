from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./test.db"  # Replace with your database file path

engine = create_engine(DATABASE_URL, echo=True)
session = Session(engine)


def create_tables():
    SQLModel.metadata.create_all(engine)

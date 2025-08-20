import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("password")

DATABASE_URL = f"mysql+pymysql://root:{password}@127.0.0.1/USERDB"

engine = create_engine(DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
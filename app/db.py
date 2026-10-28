import os
from collections.abc import Generator
from pathlib import Path

from dotenv import load_dotenv
from sqlmodel import Session, create_engine


load_dotenv(Path(__file__).resolve().parents[1] / ".env")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://127.0.0.1:5432/compras",
)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session



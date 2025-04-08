from sqlmodel import SQLModel, create_engine, Session  # noqa: F401
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session

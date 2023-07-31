from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from core.config import settings

SQLALCHEMY_DARABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DARABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False,bind=engine) #flush() changes are in a pending state (no db statements are issued yet), and can be undone by rollback() ; commits are persisted to db and non-reversible.


def get_db() -> Generator:   #dependency injection for test database....unit test
    try:
        db = sessionlocal()
        yield db
    finally:
        db.close()
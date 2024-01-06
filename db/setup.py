from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .channel import metadata


def db_setup(url: str) -> Session:

    engine = create_engine(url=url)

    Session = sessionmaker()
    Session.configure(bind=engine)

    metadata.create_all(bind=engine)

    return Session()
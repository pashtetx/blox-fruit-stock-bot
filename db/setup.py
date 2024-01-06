from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .channel import metadata
import logging


def db_setup(url: str) -> Session:

    logging.info("Initializing db...")

    engine = create_engine(url=url)

    Session = sessionmaker()
    Session.configure(bind=engine)

    metadata.create_all(bind=engine)

    logging.info("DB initialized!")

    return Session()
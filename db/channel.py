from sqlalchemy import MetaData
from sqlalchemy import Table, Integer, BigInteger, Boolean, Column
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging


metadata = MetaData()

channel = Table(
    "channels",
    metadata,
    Column("channel_id", BigInteger, primary_key=True, nullable=False),
    Column("common", Boolean, default=False),
    Column("uncommon", Boolean, default=False),
    Column("rare", Boolean, default=True),
    Column("legendary", Boolean, default=True),
    Column("mythical", Boolean, default=True),
)


def get_channels(session: Session):

    logging.info("[DB] Get channels started...")
    queryset = channel.select()
    result = session.execute(queryset)
    logging.info("[DB] Successfully got result!")
    return result

def create_channel(session: Session, channel_id: int):
    logging.info("[DB] Create channel started...")
    logging.info(f"[DB] Channel data: channel_id={channel_id}")
    queryset = channel.insert().values(channel_id=channel_id)
    select_queryset = channel.select().where(channel.c.channel_id == channel_id)

    if not session.execute(select_queryset).fetchone():
        result = session.execute(queryset)
        logging.info("[DB] Commiting database...")
        session.commit()
        logging.info("[DB] Database commited!")
        session.flush()
        logging.info("[DB] Successfully got result!")
        return result
    logging.info("[DB] Channel already exists!")

def delete_channel(session: Session, channel_id: int):
    logging.info("[DB] Delete channels started...")

    queryset = channel.delete().where(channel.c.channel_id == channel_id)
    session.execute(queryset)

    logging.info("[DB] Successfully delete channel!")
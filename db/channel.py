from sqlalchemy import MetaData
from sqlalchemy import Table, Integer, BigInteger, Boolean, Column
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
    queryset = channel.select()
    return session.execute(queryset)

def create_channel(session: Session, channel_id: int):
    queryset = channel.insert().values(channel_id=channel_id)
    select_queryset = channel.select().where(channel.c.channel_id == channel_id)
    if not session.execute(select_queryset):
        session.execute(queryset)
        session.commit()

def delete_channel(session: Session, channel_id: int):
    queryset = channel.delete().where(channel.c.channel_id == channel_id)
    session.execute(queryset)
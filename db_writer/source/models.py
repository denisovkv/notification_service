from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, Boolean

from source import settings


engine = create_engine(settings.DATABASE_URL)
meta = MetaData()

notifications = Table(
    'notifications', meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(length=50), nullable=False),
    Column('body', Text(length=500), nullable=False),
    Column('send_to', String(length=50), nullable=False),
    Column('send_at', DateTime, nullable=False),
    Column('is_sent', Boolean, nullable=False, server_default='0'),
    Column('is_deleted', Boolean, nullable=False, server_default='0'),
)


def create_models():
    if not engine.has_table('notifications'):
        meta.create_all(engine)

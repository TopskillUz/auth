import datetime

import sqlalchemy as db
from sqlalchemy.ext.declarative import declared_attr


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = db.Column(db.Integer, primary_key=True)
    is_active: bool = db.Column(db.Boolean, unique=False, default=False)
    created_at: datetime.datetime = db.Column('created_at', db.DateTime, default=datetime.datetime.now)
    updated_at: datetime.datetime = db.Column('updated_at', db.DateTime, onupdate=datetime.datetime.now)

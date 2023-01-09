import re
import uuid

import sqlalchemy as db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from core.database import Base


class User(Base):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    last_name: str = db.Column(db.String(length=45), nullable=False)
    first_name: str = db.Column(db.String(length=45), nullable=False)
    middle_name: str = db.Column(db.String(length=45), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    photo = db.Column(db.String, nullable=True)
    is_verified = db.Column(db.Boolean, nullable=False, server_default='False')

    phone: str = db.Column(db.String(length=12), nullable=False, unique=True)

    @validates('phone')
    def validate_phone(self, key, value):
        pattern = r"^998\d{9}$"
        result = re.match(pattern, value)
        if not result:
            raise ValueError("Phone number must begin with 998 and contain only 12 numbers")
        return value


class UserAvatar(Base):
    """User avatar model."""
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id), unique=True)
    title = db.Column(db.String(128), nullable=False)
    file = db.Column(db.String(128), nullable=False)

    __tablename__ = 'user_avatar'

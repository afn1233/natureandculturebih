import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.types import TypeDecorator, CHAR
from pgvector.sqlalchemy import Vector
from database import Base


class GUID(TypeDecorator):
    """UUID type that works with both PostgreSQL and SQLite"""
    impl = CHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class User(Base):
    __tablename__ = "users"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TouristLink(Base):
    __tablename__ = "tourist_links"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WeatherUpdate(Base):
    __tablename__ = "weather_updates"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    link_id = Column(GUID, ForeignKey("tourist_links.id", ondelete="CASCADE"), nullable=False)
    weather_data = Column(Text, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
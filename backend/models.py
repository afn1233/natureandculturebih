# models.py - Database table definitions
# Each class here becomes a table in PostgreSQL

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from pgvector.sqlalchemy import Vector
from database import Base

class User(Base):
    """Users table - stores people who use the app"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TouristLink(Base):
    """Tourist links table - stores saved locations"""
    __tablename__ = "tourist_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Vector embedding for semantic search - 384 dimensions from sentence-transformers
    embedding = Column(Vector(384), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WeatherUpdate(Base):
    """Weather updates table - stores weather data received from n8n webhook"""
    __tablename__ = "weather_updates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    link_id = Column(UUID(as_uuid=True), ForeignKey("tourist_links.id", ondelete="CASCADE"), nullable=False)
    weather_data = Column(JSON, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)
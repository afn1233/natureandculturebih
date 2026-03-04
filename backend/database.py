# database.py - Sets up the PostgreSQL database connection
# We use async SQLAlchemy so the app can handle multiple requests at once

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/natureandculturebih")

# Create async engine - this is the connection to PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory - used to make database queries
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for all our database models
Base = declarative_base()

# Dependency function - gives each request its own database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
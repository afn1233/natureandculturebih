# main.py - FastAPI application entry point
# This is where the app starts and all routers are connected

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine, Base
import asyncio

# Import all routers
from routers import auth, links, chat, webhook, mcp

# Create FastAPI app
app = FastAPI(
    title="NatureAndCultureBiH API",
    description="Tourist location manager for Bosnia and Herzegovina",
    version="1.0.0"
)

# Allow frontend to talk to backend
# CORS = Cross Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect all routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(links.router, prefix="/links", tags=["Links"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])
app.include_router(mcp.router, prefix="/mcp", tags=["MCP"])


@app.on_event("startup")
async def startup():
    """Run when the app starts - create tables and enable pgvector"""
    async with engine.begin() as conn:
        # Enable pgvector extension for storing embeddings
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        # Create all tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully")


@app.get("/")
async def root():
    return {"message": "NatureAndCultureBiH API is running!"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
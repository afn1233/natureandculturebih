# schemas.py - Defines the shape of data coming in and going out of the API
# Pydantic validates all data automatically

from pydantic import BaseModel, EmailStr
from typing import Optional, Any
from datetime import datetime
import uuid


# ── Auth schemas ──────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Weather schemas ───────────────────────────────────────
class WeatherResponse(BaseModel):
    id: uuid.UUID
    link_id: uuid.UUID
    weather_data: Any
    received_at: datetime

    class Config:
        from_attributes = True


# ── Tourist Link schemas ──────────────────────────────────
class LinkCreate(BaseModel):
    url: str
    title: str
    description: Optional[str] = None


class LinkUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None


class LinkResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    url: str
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    latest_weather: Optional[WeatherResponse] = None

    class Config:
        from_attributes = True


# ── Chat schemas ──────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    user_id: uuid.UUID


class ChatResponse(BaseModel):
    response: str


# ── Webhook schemas ───────────────────────────────────────
class WeatherWebhookRequest(BaseModel):
    link_id: uuid.UUID
    weather_data: Any


# ── MCP schemas ───────────────────────────────────────────
class MCPStatsResponse(BaseModel):
    total_links: int
    most_recent_link: Optional[dict] = None
    total_weather_updates: int
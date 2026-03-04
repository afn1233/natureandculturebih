# mcp.py - Model Context Protocol stats endpoint
# MCP is a protocol that allows AI agents to query external data sources
# This endpoint simulates an MCP tool that an AI agent can call
# to get statistics about a user's saved locations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid

from database import get_db
from models import TouristLink, WeatherUpdate
from schemas import MCPStatsResponse

router = APIRouter()


@router.get("/stats", response_model=MCPStatsResponse)
async def get_stats(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Get statistics about a user's saved locations.
    This endpoint follows the Model Context Protocol pattern -
    an external AI agent can call this to understand user context
    before answering questions or making recommendations.
    """
    try:
        # Count total links for this user
        count_result = await db.execute(
            select(func.count(TouristLink.id))
            .where(TouristLink.user_id == user_id)
        )
        total_links = count_result.scalar()

        # Get most recently added link
        recent_result = await db.execute(
            select(TouristLink)
            .where(TouristLink.user_id == user_id)
            .order_by(TouristLink.created_at.desc())
            .limit(1)
        )
        recent_link = recent_result.scalar_one_or_none()

        most_recent = None
        if recent_link:
            most_recent = {
                "title": recent_link.title,
                "url": recent_link.url,
                "created_at": str(recent_link.created_at)
            }

        # Count total weather updates across all user's links
        weather_result = await db.execute(
            select(func.count(WeatherUpdate.id))
            .join(TouristLink, WeatherUpdate.link_id == TouristLink.id)
            .where(TouristLink.user_id == user_id)
        )
        total_weather_updates = weather_result.scalar()

        return {
            "total_links": total_links,
            "most_recent_link": most_recent,
            "total_weather_updates": total_weather_updates
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# webhook.py - Receives weather updates from n8n automation
# n8n is an automation tool that can send weather data to this endpoint
# No authentication needed - this is a public webhook endpoint

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import WeatherUpdate, TouristLink
from schemas import WeatherWebhookRequest

router = APIRouter()


@router.post("/weather")
async def receive_weather(
    request: WeatherWebhookRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Receive weather data from n8n webhook.
    n8n sends weather updates for tourist locations automatically.
    """
    try:
        # Verify the link exists before saving weather data
        result = await db.execute(
            select(TouristLink).where(TouristLink.id == request.link_id)
        )
        link = result.scalar_one_or_none()

        if not link:
            raise HTTPException(status_code=404, detail="Tourist link not found")

        # Save weather update to database
        weather_update = WeatherUpdate(
            link_id=request.link_id,
            weather_data=request.weather_data
        )
        db.add(weather_update)
        await db.commit()

        return {"status": "ok"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
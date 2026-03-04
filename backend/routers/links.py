from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
import uuid

from database import get_db
from models import TouristLink, WeatherUpdate
from schemas import LinkCreate, LinkUpdate, LinkResponse
from embeddings import generate_embedding

router = APIRouter()


async def get_current_user_id(x_user_id: str = Header(...)) -> uuid.UUID:
    try:
        return uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")


@router.get("", response_model=list[LinkResponse])
async def get_links(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(TouristLink)
            .where(TouristLink.user_id == user_id)
            .order_by(desc(TouristLink.created_at))
        )
        links = result.scalars().all()

        links_with_weather = []
        for link in links:
            weather_result = await db.execute(
                select(WeatherUpdate)
                .where(WeatherUpdate.link_id == link.id)
                .order_by(desc(WeatherUpdate.received_at))
                .limit(1)
            )
            latest_weather = weather_result.scalar_one_or_none()

            link_dict = {
                "id": link.id,
                "user_id": link.user_id,
                "url": link.url,
                "title": link.title,
                "description": link.description,
                "created_at": link.created_at,
                "updated_at": link.updated_at,
                "latest_weather": latest_weather
            }
            links_with_weather.append(link_dict)

        return links_with_weather

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=LinkResponse)
async def create_link(
    link_data: LinkCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    try:
        text_to_embed = f"{link_data.title} {link_data.description or ''} {link_data.url}"
        embedding = await generate_embedding(text_to_embed)

        new_link = TouristLink(
            user_id=user_id,
            url=link_data.url,
            title=link_data.title,
            description=link_data.description,
            embedding=embedding
        )
        db.add(new_link)
        await db.commit()
        await db.refresh(new_link)

        return {
            "id": new_link.id,
            "user_id": new_link.user_id,
            "url": new_link.url,
            "title": new_link.title,
            "description": new_link.description,
            "created_at": new_link.created_at,
            "updated_at": new_link.updated_at,
            "latest_weather": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{link_id}", response_model=LinkResponse)
async def update_link(
    link_id: uuid.UUID,
    link_data: LinkUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(TouristLink)
            .where(TouristLink.id == link_id)
            .where(TouristLink.user_id == user_id)
        )
        link = result.scalar_one_or_none()

        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        if link_data.url is not None:
            link.url = link_data.url
        if link_data.title is not None:
            link.title = link_data.title
        if link_data.description is not None:
            link.description = link_data.description

        text_to_embed = f"{link.title} {link.description or ''} {link.url}"
        link.embedding = await generate_embedding(text_to_embed)

        await db.commit()
        await db.refresh(link)

        return {
            "id": link.id,
            "user_id": link.user_id,
            "url": link.url,
            "title": link.title,
            "description": link.description,
            "created_at": link.created_at,
            "updated_at": link.updated_at,
            "latest_weather": None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{link_id}", status_code=204)
async def delete_link(
    link_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(TouristLink)
            .where(TouristLink.id == link_id)
            .where(TouristLink.user_id == user_id)
        )
        link = result.scalar_one_or_none()

        if not link:
            raise HTTPException(status_code=404, detail="Link not found")

        await db.delete(link)
        await db.commit()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import anthropic
import os
import json
import hashlib
import math

from database import get_db
from models import TouristLink
from schemas import ChatRequest, ChatResponse

router = APIRouter()

client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def compute_embedding(text: str) -> list:
    embedding = []
    for i in range(1536):
        hash_input = f"{text}_{i}".encode("utf-8")
        hash_val = int(hashlib.sha256(hash_input).hexdigest(), 16)
        val = (hash_val % 1000000) / 500000.0 - 1.0
        embedding.append(val)
    magnitude = math.sqrt(sum(x**2 for x in embedding))
    if magnitude > 0:
        embedding = [x / magnitude for x in embedding]
    return embedding


def cosine_similarity(a: list, b: list) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x**2 for x in a))
    mag_b = math.sqrt(sum(x**2 for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0
    return dot / (mag_a * mag_b)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Get all user links
        result = await db.execute(
            select(TouristLink).where(TouristLink.user_id == request.user_id)
        )
        links = result.scalars().all()

        # Find most similar links using cosine similarity
        query_embedding = compute_embedding(request.message)
        scored_links = []

        for link in links:
            if link.embedding:
                try:
                    link_embedding = json.loads(link.embedding)
                    score = cosine_similarity(query_embedding, link_embedding)
                    scored_links.append((score, link))
                except:
                    pass

        # Sort by similarity and take top 3
        scored_links.sort(key=lambda x: x[0], reverse=True)
        top_links = [link for _, link in scored_links[:3]]

        if top_links:
            context = "\n\n".join([
                f"Location: {link.title}\nURL: {link.url}\nDescription: {link.description or 'No description'}"
                for link in top_links
            ])
        else:
            context = "No saved locations found."

        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=f"""You are a helpful travel assistant for Bosnia and Herzegovina.
Answer based on the following saved locations the user has added.
Be concise, friendly and informative.

Saved locations:
{context}""",
            messages=[{"role": "user", "content": request.message}]
        )

        return {"response": message.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

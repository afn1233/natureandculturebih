# chat.py - Handles AI chat using RAG (Retrieval Augmented Generation)
# RAG works like this:
# 1. Convert user question to embedding (numbers)
# 2. Find the most similar saved links using vector search
# 3. Send those links as context to Claude AI
# 4. Claude answers based on the actual saved locations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
import anthropic
import os

from database import get_db
from models import TouristLink
from schemas import ChatRequest, ChatResponse
from embeddings import generate_embedding

router = APIRouter()

# Initialize Anthropic client
client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Chat with AI about saved tourist locations.
    Uses vector similarity search to find relevant links first.
    """
    try:
        # Step 1: Generate embedding for the user's question
        query_embedding = await generate_embedding(request.message)

        # Step 2: Find the 3 most similar links using pgvector cosine similarity
        # The <=> operator calculates cosine distance between vectors
        # Lower distance = more similar content
        # ORDER BY embedding <=> query_embedding LIMIT 3
        similarity_query = text("""
            SELECT id, title, description, url
            FROM tourist_links
            WHERE user_id = :user_id
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT 3
        """)

        result = await db.execute(
            similarity_query,
            {
                "user_id": str(request.user_id),
                "embedding": str(query_embedding)
            }
        )
        similar_links = result.fetchall()

        # Step 3: Build context from similar links
        if similar_links:
            context = "\n\n".join([
                f"Location: {link.title}\nURL: {link.url}\nDescription: {link.description or 'No description'}"
                for link in similar_links
            ])
        else:
            context = "No saved locations found."

        # Step 4: Call Claude API with context
        message = await client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=f"""You are a helpful travel assistant for Bosnia and Herzegovina.
Answer based only on the following saved locations the user has added.
Be concise, friendly and informative.

Saved locations:
{context}""",
            messages=[
                {"role": "user", "content": request.message}
            ]
        )

        return {"response": message.content[0].text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
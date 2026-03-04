# auth.py - Handles user login
# No passwords needed - just email based authentication
# If email exists return the user, if not create a new one

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import User
from schemas import LoginRequest, UserResponse

router = APIRouter()


@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Login or register with just an email address.
    No password needed - this keeps things simple for the app.
    """
    try:
        # Check if user already exists
        result = await db.execute(
            select(User).where(User.email == request.email)
        )
        user = result.scalar_one_or_none()

        if user:
            # User exists - return their data
            return user
        
        # User doesn't exist - create a new one
        new_user = User(email=request.email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
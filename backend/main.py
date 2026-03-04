from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, links, chat, webhook, mcp

app = FastAPI(title="NatureAndCultureBiH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(links.router, prefix="/links")
app.include_router(chat.router, prefix="/chat")
app.include_router(webhook.router, prefix="/webhook")
app.include_router(mcp.router, prefix="/mcp")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully")


@app.get("/health")
async def health():
    return {"status": "healthy"}

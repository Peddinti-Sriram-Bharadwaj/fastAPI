from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, engine
from app.models import Base, Message
from sqlalchemy.future import select

app = FastAPI()

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get DB session
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/messages/")
async def create_message(content: str, session: AsyncSession = Depends(get_session)):
    message = Message(content=content)
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message

@app.get("/messages/")
async def read_messages(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Message))
    return result.scalars().all()

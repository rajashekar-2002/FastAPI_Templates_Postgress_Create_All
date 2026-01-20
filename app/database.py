import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔹 create_async_engine
# WHY?
# - This creates a NON-BLOCKING database connection
# - While DB is responding, FastAPI can handle other users
engine = create_async_engine(
    DATABASE_URL,
    echo=True  # shows SQL logs (good for learning)
)

# 🔹 sessionmaker creates DB session factory
# WHY AsyncSession?
# - Normal Session blocks
# - AsyncSession works with await
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for all database models
Base = declarative_base()

# 🔹 Dependency for FastAPI
# WHY async + yield?
# - Creates DB session per request
# - Closes session automatically after request ends
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

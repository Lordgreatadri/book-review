from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src.config import Config


# Define async database URL
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{Config.database_username}:{Config.database_password}@{Config.database_hostname}:{Config.database_port}/{Config.database_name}"

# Create async engine object here
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# Create an async sessionmaker
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
 

async def init_db():
    async with engine.begin() as conn:
        # Use run_sync for synchronous operations inside async functions
        await conn.run_sync(SQLModel.metadata.create_all)

# async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL))

async def get_session()->AsyncSession: # type: ignore
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )  

    async with Session() as session:
        try:
            yield session 
        finally:
            await session.close()         
import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

load_dotenv()

SQLA_DB = os.getenv("FASTAPI_DB_URL")

async_engine = create_async_engine(SQLA_DB, connect_args={"check_same_thread": False})

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


class AsyncDBContext:
    def __init__(self):
        self.db = AsyncSessionLocal()

    async def __aenter__(self):
        return self.db

    async def __aexit__(self, et, ev, traceback):
        await self.db.close()


async def get_db() -> AsyncSession:
    async with AsyncDBContext() as db:
        yield db
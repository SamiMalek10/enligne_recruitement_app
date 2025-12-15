from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis
from app.config import settings


class Database:
    client: AsyncIOMotorClient = None
    redis_client: Redis = None


db = Database()


async def get_database():
    """Get MongoDB database"""
    return db.client[settings.DATABASE_NAME]


def get_redis():
    """Get Redis client"""
    return db.redis_client


async def connect_to_database():
    """Connect to MongoDB and Redis"""
    print("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    print("Connecting to Redis...")
    db.redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    print("Connected to databases successfully!")


async def close_database_connection():
    """Close database connections"""
    print("Closing database connections...")
    if db.client:
        db.client.close()
    if db.redis_client:
        db.redis_client.close()
    print("Database connections closed.")

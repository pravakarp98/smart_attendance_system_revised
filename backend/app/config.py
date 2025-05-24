import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE URL", "mongodb://localhost:27017/org_db")
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key")
    API_KEY = os.getenv("API_KEY", "internal_api_key")
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/60")
    JWT_EXPIRATION_TIME = int(os.getenv("JWT_EXPIRATION_TIME", "3600"))
    
settings = Settings()
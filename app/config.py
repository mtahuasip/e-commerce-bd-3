import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/e_commerce")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    CART_DURATION = int(os.getenv("CART_DURATION", 60))

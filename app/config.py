import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env from root project directory

class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_NAME = os.getenv("DB_NAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_USER = os.getenv("DB_USER")

    DATEBASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    ZOOKEEPER_HOST = os.getenv("ZOOKEEPER_HOST")
    ZOOKEEPER_PORT = os.getenv("ZOOKEEPER_PORT")
    ZOOKEEPER_RANGE_GAP = 10000

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
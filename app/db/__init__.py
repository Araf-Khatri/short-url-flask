from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import Config
from app.db.base import Base

engine = create_engine(Config.DATEBASE_URI)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()
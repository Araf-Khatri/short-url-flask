from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from ..base import Base

class Url(Base):
  __tablename__  = "urls"
  
  id = Column(Integer, autoincrement=True, primary_key=True, index=True)
  short_url = Column(String, nullable=False, unique=True)
  long_url = Column(String, nullable=False)
  base10_integer = Column(Integer, nullable=False)
  created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
  expires_at = Column(DateTime, nullable=True)

  def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

from redis import ConnectionPool, Redis
from ..config import Config

class RedisCache:
  def __init__(self) -> None:
    pool = ConnectionPool(
      host=Config.REDIS_HOST,
      port=Config.REDIS_PORT,
      db=0,
      max_connections=10, 
      decode_responses=True
    )
    self.redis_client = Redis(connection_pool=pool)

redis_connection = RedisCache()
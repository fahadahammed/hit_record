#  Copyright (c) Fahad Ahammed 2024.
import redis
from src import app


pool = redis.ConnectionPool(
    host=app.config.get("REDIS_HOST"),
    port=int(app.config.get("REDIS_PORT")),
    db=int(app.config.get("REDIS_DB"))
)


class RedisOps:
    def __init__(self):
        self.rc = redis.Redis(connection_pool=pool, decode_responses=True)

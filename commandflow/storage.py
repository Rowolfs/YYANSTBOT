### commandflow/storage.py

import json
from typing import Any
import redis.asyncio as redis

class BaseStorage:
    async def save(self, key: int, value: Any):
        raise NotImplementedError

    async def load(self, key: int) -> Any:
        raise NotImplementedError

    async def delete(self, key: int):
        raise NotImplementedError


class MemoryStorage(BaseStorage):
    def __init__(self):
        self._storage = {}

    async def save(self, key: int, value: Any):
        self._storage[str(key)] = json.dumps(value)

    async def load(self, key: int) -> Any:
        data = self._storage.get(str(key))
        return json.loads(data) if data else None

    async def delete(self, key: int):
        self._storage.pop(str(key), None)


class RedisStorage(BaseStorage):
    def __init__(self, redis_url="redis://localhost"):
        self.redis = redis.from_url(redis_url)

    async def save(self, key: int, value: Any):
        await self.redis.set(str(key), json.dumps(value))

    async def load(self, key: int) -> Any:
        data = await self.redis.get(str(key))
        return json.loads(data) if data else None

    async def delete(self, key: int):
        await self.redis.delete(str(key))


# По умолчанию используется MemoryStorage
storage: BaseStorage = MemoryStorage()

def use_storage(custom_storage: BaseStorage):
    global storage
    storage = custom_storage

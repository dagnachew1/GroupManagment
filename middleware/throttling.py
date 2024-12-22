from aiogram import BaseMiddleware
from aiogram.types import Update
from cachetools import TTLCache
from typing import Any, Awaitable, Callable, Dict

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: int = 1):
        self.cache = TTLCache(maxsize=10_000, ttl=1/rate_limit)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        if not event.chat or event.chat.id in self.cache:
            return
            
        self.cache[event.chat.id] = None
        return await handler(event, data)
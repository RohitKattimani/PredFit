from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._by_user: dict[int, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(self, user_id: int, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._by_user[user_id].add(ws)

    async def disconnect(self, user_id: int, ws: WebSocket) -> None:
        async with self._lock:
            self._by_user[user_id].discard(ws)

    async def broadcast_user(self, user_id: int, message: dict[str, Any]) -> None:
        async with self._lock:
            conns = list(self._by_user.get(user_id, set()))
        if not conns:
            return
        living: list[WebSocket] = []
        for ws in conns:
            try:
                await ws.send_json(message)
                living.append(ws)
            except Exception:
                pass
        async with self._lock:
            self._by_user[user_id] = set(living)


manager = ConnectionManager()


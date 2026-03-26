from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import init_db
from app.realtime import manager
from app.routers import auth, logs, risk
from app.security import decode_token


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


app.include_router(auth.router)
app.include_router(logs.router)
app.include_router(risk.router)


@app.get("/health")
def health():
    return {"ok": True, "name": settings.app_name, "env": settings.environment}


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    token = ws.query_params.get("token")
    if not token:
        await ws.close(code=4401)
        return
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except Exception:
        await ws.close(code=4401)
        return

    await manager.connect(user_id, ws)
    try:
        while True:
            # keepalive / client messages (optional)
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(user_id, ws)
    except Exception:
        await manager.disconnect(user_id, ws)


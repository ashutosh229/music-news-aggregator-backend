from fastapi import APIRouter, WebSocket
from typing import List

clients: List[WebSocket] = []

router = APIRouter()


@router.websocket("/ws")
async def websocket_entrypoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)


async def broadcast_new_article(article: dict):
    to_remove = []
    for client in clients:
        try:
            await client.send_json(article)
        except:
            to_remove.append(client)
    for client in to_remove:
        clients.remove(client)

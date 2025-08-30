from fastapi import APIRouter, WebSocket
from typing import List
from starlette.websockets import WebSocketDisconnect

clients: List[WebSocket] = set()

router = APIRouter(prefix="/websocket")


## http://127.0.0.1:8080/websocket
@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print(f"New client connected. Total clients: {len(clients)}")
    try:
        while True:
            msg = await websocket.receive_text()
            print(f"Received from client: {msg}")
    except WebSocketDisconnect:
        clients.discard(websocket)
        print(f"Client disconnected. Total clients: {len(clients)}")


async def broadcast_new_article(article: dict):
    print(f"Broadcasting article: {article} to {len(clients)} clients")
    disconnected = []
    for client in clients:
        try:
            await client.send_json(article)
        except:
            disconnected.append(client)
    for client in disconnected:
        clients.discard(client)

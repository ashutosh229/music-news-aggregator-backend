from fastapi import APIRouter, WebSocket
from typing import List

clients: List[WebSocket] = []

router = APIRouter()

@router.websocket("/ws")
async def websocket_entrypoint(websocket: WebSocket):
    pass 

async def broadcast_new_article(article: dict):
    for client in clients:
        await client.send_json(article)
        

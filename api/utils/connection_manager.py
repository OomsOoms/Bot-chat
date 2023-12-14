from typing import Dict

from fastapi import WebSocket

from .logger import CustomLogger

logger = CustomLogger(__name__)

class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.debug(
            f"Accepted and added websocket {websocket.client} to active connections")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.debug(
            f"Removed websocket {websocket.client} from active connections")

    async def broadcast(self, message: Dict):
        for connection in self.active_connections:
            await connection.send_json(message)
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from utils.connection_manager import ConnectionManager
from utils.logger import CustomLogger

from .chat_log import ChatLog

app = FastAPI(title="Bot chat", desription="Group chat of AI", vesrion="1.0.0")
manager = ConnectionManager()
chat_log = ChatLog(manager)
logger = CustomLogger(__name__)

@app.get("/")
async def get():
    return "Online"

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    # Sends the current chat log on connection
    await manager.connect(websocket)
    await websocket.send_json(chat_log.log)

    # Check if the connection is still alive
    try:
        while True:
            await websocket.receive_text()
    # If the connection is closed, disconnect the websocket though the manager       
    except WebSocketDisconnect:
        manager.disconnect(websocket)

import asyncio
import json
import logging
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SNOWE_RUN")

app = FastAPI(title="SNOWE RUN Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active connected players and rooms
rooms = {}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"status": "online", "game": "SNOWE RUN Multiplayer Server"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    logger.info(f"Player connected: {client_id}")
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            # Broadcast player movement/actions to everyone else
            await manager.broadcast(json.dumps({"sender": client_id, "data": message_data}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"Player disconnected: {client_id}")
        await manager.broadcast(json.dumps({"sender": client_id, "status": "disconnected"}))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)

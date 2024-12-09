import uuid
import json
from fastapi import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed

class WebSocketUpdater:
    def __init__(self):
        self.sockets: dict[str, dict[str, WebSocket]] = {} #sockets[subscribe_id][socket_id]の順にアクセス

    async def subscribe(self, subscribe_id: str, websocket: WebSocket):
        await websocket.accept()
        socket_id = uuid.uuid4().hex

        if self.sockets.get(subscribe_id) is None:
            self.sockets[subscribe_id] = {}

        self.sockets[subscribe_id][socket_id] = websocket

        try:
            while True:
                await websocket.receive_text()
        except (WebSocketDisconnect, ConnectionClosed):
            del self.sockets[subscribe_id][socket_id]
            if len(self.sockets[subscribe_id]) == 0:
                del self.sockets[subscribe_id]
            print("CLIENT DISCONNECTED")

    async def broadcast(self, subscribe_id: str, data: dict):
        # print(len(self.sockets[subscribe_id]), subscribe_id)
        if self.sockets.get(subscribe_id) is not None:
            for websocket in self.sockets[subscribe_id].values():
                await websocket.send_text(json.dumps(data))

updater = WebSocketUpdater()

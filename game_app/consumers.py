import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called when the WebSocket is handshaking as part of the connection process.
        await self.accept()

    async def disconnect(self, close_code):
        # Called when the WebSocket closes for any reason.
        pass

    async def receive(self, text_data):
        # Called when the server receives a message from the WebSocket.
        text_data_json = json.loads(text_data)

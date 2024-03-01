import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.room_group_name = f"{self.game_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

    # Receive message from room group
    def post_game_board(self, event):
        game_board = event["game_board"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "type": "post_game_board",
            "game_board": game_board,
        }))

from django.urls import re_path
from game_app.consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r'ws/game/play/$', GameConsumer.as_asgi()),
]
from django.urls import re_path
from game_app.consumers import GameConsumer

websocket_urlpatterns = [
    re_path(r'ws/post-game-board/(?P<game_id>\d+)/$', GameConsumer.as_asgi())
]
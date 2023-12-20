from django.urls import path, re_path
from .views import play_game
from game_app import consumers


urlpatterns = [
    path('play/', play_game, name='play_game'),
]

websocket_urlpatterns = [
    re_path(r'ws/game/$', consumers.GameConsumer.as_asgi()),
]

from django.urls import path
from game_app.v2.views import game_play, game_over, game_home

urlpatterns = [
    path("home/", game_home, name="game_home"),
    path("play/<int:board_id>/<int:player_game_id>/", game_play, name="game_play"),
    path("game_over/<int:board_id>/<int:player_game_id>/", game_over, name="game_over"),
]

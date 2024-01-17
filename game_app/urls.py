from django.urls import path
from .v2.views import play_game, game_over

urlpatterns = [
    path("game_over/", game_over, name="game_over"),
    path("play/", play_game, name="play_game"),
]

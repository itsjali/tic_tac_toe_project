from django.urls import path

from game_app.v2.views import new_game, active_games, game_play, game_over, game_home, signup_view, login_view


urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", login_view, name="logout"),
    path("signup/", signup_view, name="signup"),
    path("home/", game_home, name="game_home"),
    path("new_game/<int:opponent_user_id>/", new_game, name="new_game"),
    path("active_games/<int:game_id>/", active_games, name="active_games"),
    path("play/<int:game_id>/<int:player_id>/", game_play, name="game_play"),
    path("game_over/<int:game_id>/", game_over, name="game_over"),
]

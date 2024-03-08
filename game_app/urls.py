from django.urls import path

from game_app.v2 import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.login_view, name="logout"),
    path("home/", views.game_home, name="game_home"),
    path("new_game/<int:opponent_user_id>/", views.new_game, name="new_game"),
    path("active_games/<int:game_id>/", views.active_games, name="active_games"),
    path("play/<int:game_id>/<int:player_id>/", views.game_play, name="game_play"),
    path("game_over/<int:game_id>/", views.game_over, name="game_over"),
]

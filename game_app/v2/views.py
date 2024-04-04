import json
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from game_app.v2.forms import PlayerInputForm, CreateUserForm, LoginForm
from game_app.v2.models import Game
from game_app.v2.services import (
    check_winner, 
    check_board_full,
    create_new_game,
    get_active_game,
    get_player_icon,
    switch_active_player,
    update_board,
    CellAlreadyFilled,
    InvalidActiveUser,
    InvalidCredentials,
    InvalidCreateUserCredentials,
    authenticate_login_user,
)

# Authentication

def signup_view(request):
    if request.method == "POST":
        try: 
            form = CreateUserForm(request.POST)
            if form.is_valid():
                return redirect("login")
            
        except InvalidCreateUserCredentials as e:
            error_message = e
            return render(request, "game_app/signup.html", {"error_message": error_message})

    form = CreateUserForm()

    context = {
        "form": form,
        "signup_page": True,
    }
    return render(request, "game_app/signup.html", context)


def login_view(request):
    if request.method == "POST":
        try:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data
                login(request, username)
                return redirect("game_home")
            
        except InvalidCredentials as e:
            error_message = e
            return render(request, "game_app/login.html", {"error_message": error_message})

    form = LoginForm()
    
    context = {
        "form": form,
        "login_page": True,
    }
    return render(request, "game_app/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


# Game Views

@authenticate_login_user
def game_home(request):
    user = request.user
    opponent_users = User.objects.exclude(id=user.id)
    active_games = Game.objects.filter(
        Q(player_1=user, is_active=True) | 
        Q(player_2=user, is_active=True)
    )

    active_game_info = []
    for game in active_games:
        opponent = game.player_1 if game.player_1 != user else game.player_2
        active_game_info.append({
            'opponent_username': opponent.username,
            'game_id': game.id
        })

    context = {
        "opponent_users": opponent_users,
        "active_game_info": active_game_info,
    }

    return render(request, "game_app/home.html", context)


@authenticate_login_user
def new_game(request, opponent_user_id):
    try:
        game = create_new_game(request, opponent_user_id)
        return redirect("game_play", game.id, game.player_1.id)
    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect("game_home")


@authenticate_login_user
def active_games(request, game_id):
    game = get_active_game(game_id)
    return redirect("game_play", game.id, request.user.id)


@authenticate_login_user
def game_play(request, game_id, player_id):
    game = Game.objects.get(pk=game_id)
    game_board = json.loads(game.board)
    
    user = User.objects.get(pk=player_id)
    player_icon = get_player_icon(game, user)

    error_message = ""
    game_over_outcome = False
    
    if request.method == 'POST':
        try:
            form = PlayerInputForm(request.POST, game=game, user=user)
            if form.is_valid():
                row, col = form.cleaned_data
                updated_game_board = update_board(row, col, game_board, player_icon)
                game.board = json.dumps(updated_game_board)
                switch_active_player(game, user)

                if check_winner(updated_game_board, player_icon):
                    game.outcome = f"{user} Wins"
                
                if check_board_full(updated_game_board):
                    game.outcome = "A Draw"
                
                if not game.outcome:
                    game.board = json.dumps(updated_game_board)
                    switch_active_player(game, user)
                
                game.save()

        except CellAlreadyFilled as e:
            error_message = e
        
        except InvalidActiveUser as e:
            error_message = e

    form = PlayerInputForm()

    context = {
        "game_board": game_board,
        "error_message": error_message,
        "form": form,
        "game_over": game_over_outcome,
        "game": game,
        "player_id": player_id
    }

    if game.outcome:
        return redirect("game_over", game_id)

    return render(request, "game_app/play.html", context)


@authenticate_login_user
def game_over(request, game_id):
    game = Game.objects.get(pk=game_id)
    game.is_active = False
    game.save()

    if request.method == "POST":
        return redirect("game_home")
    
    context = {
        "outcome_message": game.outcome, 
        "game_id": game_id,
        "game_outcome": game.outcome, 
        "winner_outcome": f"{user} Wins",
        "draw_outcome": "A Draw",
    }

    return render(request, "game_app/game_over.html", context)
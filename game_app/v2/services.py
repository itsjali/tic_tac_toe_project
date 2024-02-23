from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from game_app.v2.models import Game


# Game Functions

def check_winner(game_board, player_symbol):
    # Check rows
    for row in game_board:
        if all(cell == player_symbol for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(game_board[row][col] == player_symbol for row in range(3)):
            return True
        
    # Check diagonal
    if all(game_board[i][i] == player_symbol for i in range(3)):
        return True
    
    # Check opposite diagonal
    if all(game_board[i][2 - i] == player_symbol for i in range(3)):
        return True


def check_board_full(game_board):
    for row in game_board:
        for cell in row:
            if cell == "":
                return False
    return True


def update_board(row, col, game_board, player_symbol):
    game_board[row][col] = player_symbol
    return game_board


def create_new_game(request, opponent_user_id):
    player_1 = User.objects.get(id=request.user.id)
    player_2 = User.objects.get(id=opponent_user_id)

    if Game(player_1=player_1, player_2=player_2).has_active_game:
        raise ValidationError(
            f"Unable to create new game. Please complete your active game with {player_2}."
        )
    
    game = Game.objects.create(
        player_1=player_1,
        player_2=player_2,
        active_player=player_1
    )
    return game


def get_active_game(game_id):
    game = Game.objects.get(id=game_id)
    return game


def get_player_icon(game, user):
    if user == game.player_1:
        return game.player_1_icon
    if user == game.player_2:
        return game.player_2_icon
    

def switch_active_player(game, user):
    if user == game.player_1:
        game.active_player = game.player_2
    
    if user == game.player_2:
        game.active_player = game.player_1

    game.save()


# Custom Errors

class CellAlreadyFilled(ValueError):
    pass


class InvalidCredentials(ValueError):
    pass


class InvalidCreateUserCredentials(ValueError):
    pass


class InvalidActiveUser(ValueError):
    pass


def authenticate_login_user(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return view_func(request, *args, **kwargs)

    return wrapper
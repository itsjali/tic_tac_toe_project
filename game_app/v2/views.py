import json

from django.shortcuts import render

from game_app.v2.forms import PlayerInputForm
from game_app.v2.models import GameData
from game_app.v2.services import (
    check_winner, 
    check_board_full,
    create_new_game_data,
    reset_game_data,
    update_board,
    which_player,
    CellAlreadyFilled,
)


def game_over(request, outcome_message=None):
    if "reset" in request.GET:
        new_game_data = reset_game_data(request)
        return play_game(request, game_data=new_game_data)

    context = {"outcome_message": outcome_message}
    return render(request, "game_app/game_over.html", context)


def play_game(request, game_data=None):
    game_data_id = request.session.get("game_data_id")

    if not game_data_id:
        game_data = create_new_game_data()
    else:
        game_data = GameData.objects.get(id=game_data_id)
    
    if "reset" in request.GET:
        game_data = reset_game_data(request)

    game_board = json.loads(game_data.board)
    current_player = game_data.current_player
    error_message = ""
    outcome_message = ""
    game_over_outcome = False
    
    if request.method == 'POST':
        try:
            form = PlayerInputForm(request.POST, game_board=game_board)

            if form.is_valid():
                row, col = form.cleaned_data
                updated_game_board = update_board(row, col, game_board, current_player)

                if check_board_full(updated_game_board):
                    outcome_message = "It's a Draw!"
                    game_over_outcome = True
                
                elif check_winner(updated_game_board, current_player):
                    player = which_player(current_player)
                    outcome_message = f"{player} Wins!"
                    game_over_outcome = True

                if not game_over_outcome: 
                    if game_data.current_player == "O":
                        game_data.current_player = "X" 
                    else: 
                        game_data.current_player = "O"
                    
                    game_data.board = json.dumps(updated_game_board)
                    game_data.save()

        except CellAlreadyFilled as e:
            error_message = e

    form = PlayerInputForm()

    context = {
        "game_board": game_board,
        "error_message": error_message,
        "outcome_message": outcome_message,
        "form": form,
        "game_over": game_over_outcome,
    }

    if game_over_outcome:
        return game_over(request, outcome_message=outcome_message)

    return render(request, "game_app/play_game.html", context)
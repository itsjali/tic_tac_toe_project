import json

from django.shortcuts import render, redirect

from game_app.v2.forms import PlayerInputForm
from game_app.v2.models import GameBoard, Players
from game_app.v2.services import (
    check_winner, 
    check_board_full,
    create_game_data,
    reset_board_data,
    update_board,
    which_player,
    CellAlreadyFilled,
)


def game_home(request):
    if request.method == "POST":
        game_data = create_game_data()
        return redirect("game_play", game_data[0].id, game_data[1])

    return render(request, "game_app/home.html")


def game_play(request, board_id, player_game_id):
    if "reset" in request.GET:
        game_board = reset_board_data(board_id)

    game_board_obj = GameBoard.objects.get(id=board_id)
    player_obj = Players.objects.get(player_game_id=player_game_id, game_board=game_board_obj)

    game_board = json.loads(game_board_obj.data)
    player_symbol = player_obj.symbol
    error_message = ""
    game_over_outcome = False
    
    if request.method == 'POST':
        try:
            form = PlayerInputForm(request.POST, game_board=game_board)

            if form.is_valid():
                row, col = form.cleaned_data
                updated_game_board = update_board(row, col, game_board, player_symbol)

                if check_board_full(updated_game_board) or check_winner(updated_game_board, player_symbol):
                    game_over_outcome = True
                    
                game_board_obj.data = json.dumps(updated_game_board)
                game_board_obj.save()

        except CellAlreadyFilled as e:
            error_message = e

    form = PlayerInputForm()

    context = {
        "game_board": game_board,
        "error_message": error_message,
        "form": form,
        "game_over": game_over_outcome,
        "board_id": board_id,
        "player_game_id": player_game_id
    }

    if game_over_outcome:
        return redirect("game_over", board_id, player_game_id)

    return render(request, "game_app/play.html", context)


def game_over(request, board_id, player_game_id):
    game_board_obj = GameBoard.objects.get(id=board_id)
    player_obj = Players.objects.get(game_board=game_board_obj, player_game_id=player_game_id)

    if request.method == "POST":
        reset_board_data(board_id)
        return redirect("game_play", board_id, player_game_id)
    
    if check_board_full(game_board_obj.data):
        outcome_message = "It's a Draw!"

    if check_winner(game_board_obj.data, player_obj.symbol):
        player_ = which_player(player_obj.symbol)
        outcome_message = f"{player_} Wins!"
    
    context = {
        "outcome_message": outcome_message, 
        "board_id": board_id,
        "player_game_id": player_game_id,
    }
    return render(request, "game_app/game_over.html", context)
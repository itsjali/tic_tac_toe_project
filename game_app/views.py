from django.shortcuts import render
from game_app.forms import PlayerInputForm
from game_app.services import CellAlreadyFilled, GameFinished


def check_winner(game_board, current_player):
    # Check rows
    for row in game_board:
        if all(cell == current_player for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(game_board[row][col] == current_player for row in range(3)):
            return True
        
    # Check diagonal
    if all(game_board[i][i] == current_player for i in range(3)):
        return True
    
    # Check opposite diagonal
    if all(game_board[i][2 - i] == current_player for i in range(3)):
        return True


def check_board_full(game_board):
    for row in game_board:
        for cell in row:
            if cell == "":
                return False
    return True


def which_player(current_player):
    if current_player == "O":
        return "Player 1"
    else:
        return "Player 2"


def play_game(request):
    if "reset" in request.GET or not request.session.get("game_board"):
        request.session["game_board"] = [["", "", ""], ["", "", ""], ["", "", ""]]
        request.session["current_player"] = "O"

    game_board = request.session["game_board"]
    current_player = request.session["current_player"]
    error_message = ""
    outcome_message = ""

    if request.method == 'POST':
        try:
            form = PlayerInputForm(request.POST, game_board=game_board, current_player=current_player)
            
            if form.is_valid():
                row, col = form.cleaned_data
                game_board[row][col] = current_player

                # add a functionality that stops the user from inputting when the game is over
                # consider redirecting or hide input form
                if check_board_full(game_board):
                    outcome_message = "It's a Draw!"
            
                if check_winner(game_board, current_player):
                    player = which_player(current_player)
                    outcome_message = f"{player} Wins!"
                
                if current_player == "O":
                    request.session["current_player"] = "X"
                else:
                    request.session["current_player"] = "O"
        
        except CellAlreadyFilled as e:
            error_message = e

        except ValueError as e:
            error_message = e

    form = PlayerInputForm()

    context = {
        "game_board": game_board,
        "error_message": error_message,
        "outcome_message": outcome_message,
        "form": form,
    }

    return render(request, 'game_app/play_game.html', context)
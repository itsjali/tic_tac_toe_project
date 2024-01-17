from game_app.v2.models import GameData


# Game Functions

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


def update_board(row, col, game_board, current_player):
    game_board[row][col] = current_player
    return game_board


def reset_game_data(request):
    game_data = GameData.objects.create()
    request.session["game_data_id"] = game_data.id
    return game_data


# Custom Errors

class CellAlreadyFilled(ValueError):
    pass


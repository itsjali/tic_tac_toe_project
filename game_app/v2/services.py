from game_app.v2.models import GameBoard, Players


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


def which_player(player_symbol):
    if player_symbol == "O":
        return "Player 1"
    else:
        return "Player 2"


def update_board(row, col, game_board, player_symbol):
    game_board[row][col] = player_symbol
    return game_board


def create_game_data():
    game_board = GameBoard.objects.create()
    player_1 = Players.objects.create(player_game_id=1, game_board=game_board, symbol="O")
    player_2 = Players.objects.create(player_game_id=2, game_board=game_board, symbol="X")
    return game_board, player_1.player_game_id


def reset_board_data(board_id):
    game_board = GameBoard.objects.get(id=board_id)
    game_board.data = '[["", "", ""], ["", "", ""], ["", "", ""]]'
    game_board.save()
    return game_board

# Custom Errors

class CellAlreadyFilled(ValueError):
    pass


from game_app.services import PlayGame, CellAlreadyFilled, NoInputError
import pytest

from unittest import mock


@pytest.mark.parametrize(
    "game_board, expected_full_board",
    (
        ([["X", "", ""], ["O", "X", ""], ["O", "", ""]], False), 
        ([["O", "X", "O"], ["O", "X", "X"], ["O", "O", "X"]], True), 
    ),
)
def test_check_board_full(game_board, expected_full_board):
    game = PlayGame()
    game.game_board = game_board

    assert game.check_board_full() is expected_full_board


def test_get_valid_player_input_function_with_valid_inputs():
    game = PlayGame()

    with mock.patch("builtins.input", return_value="1 3"):
        assert game.get_valid_player_input() == (0, 2)


def test_get_valid_player_input_function_with_no_input():
    game = PlayGame()

    def mock_input():
        if not hasattr(mock_input, "called"):
            setattr(mock_input, "called", True)
            return ""
        else:
            raise NoInputError("Invalid input")

    with mock.patch("builtins.input", side_effect=mock_input):
        with pytest.raises(NoInputError, match="Invalid input"):
            game.get_valid_player_input()


def test_get_valid_player_input_function_with_no_cell_already_filled():
    game = PlayGame()
    game.game_board = [["X", "", ""], ["", "", ""], ["", "", ""]]

    def mock_input():
        if not hasattr(mock_input, "called"):
            setattr(mock_input, "called", True)
            return "1 1"
        else:
            raise CellAlreadyFilled("Cell already filled")

    with mock.patch("builtins.input", side_effect=mock_input):
        with pytest.raises(CellAlreadyFilled, match="Cell already filled"):
            game.get_valid_player_input()


@pytest.mark.parametrize(
    "game_board, player, winner, check_winner",
    (
        ([["X", "X", "X"], ["O", "O", ""], ["", "", ""]], "X", "Player 2", True), # horizontal
        ([["O", "X", ""], ["O", "X", ""], ["O", "", ""]], "O", "Player 1", True), # vertical
        ([["X", "O", ""], ["O", "X", ""], ["", "", "X"]], "X", "Player 2", True), # diagonal
        ([["", "X", "O"], ["", "O", ""], ["O", "X", "X"]], "O", "Player 1", True), # opposite diagonal
    ),
)
def test_check_winner_function_if_there_is_a_winner(game_board, player, winner, check_winner, capsys):
    game = PlayGame()
    game.game_board = game_board
    game.active_player = player
    
    service = game.check_winner()
    message = capsys.readouterr()

    assert service is check_winner
    assert f"{winner} Wins!" in message.out


def test_display_its_a_draw_message_if_board_is_full_and_no_winners(capsys):
    game = PlayGame()
    game.game_board = [["O", "X", "O"], ["X", "O", "X"], ["X", "O", "X"]]
    user_input = ""

    with mock.patch("builtins.input", return_value=user_input):
        game.run()

    message = capsys.readouterr()

    assert game.check_winner() is False
    assert game.check_board_full() is True
    assert "It's a Draw!" in message.out

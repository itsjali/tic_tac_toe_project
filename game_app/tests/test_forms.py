from game_app.v2.forms import PlayerInputForm
from game_app.v1.game import CellAlreadyFilled


import pytest

def test_player_input_form_has_valid_input():
    form_data = {'row': 1, 'col': 2}
    game_board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"

    form = PlayerInputForm(data=form_data, game_board=game_board, current_player=current_player)
    assert form.is_valid()
    assert form.cleaned_data == (0, 1)


@pytest.mark.parametrize("form_data", [({'row': 7, 'col': 4}), ({'row': 0, 'col': -2})]) 
def test_player_input_form_raise_error_if_input_is_not_in_range_1_and_3(form_data):
    game_board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"

    with pytest.raises(ValueError, match="Unable to process your input. Please input two valid numbers that are between 1-3"):
        form = PlayerInputForm(data=form_data, game_board=game_board, current_player=current_player)
        form.is_valid()


def test_player_input_form_raise_error_if_cell_is_already_filled():
    form_data = {'row': 1, 'col': 2}
    game_board = [["", "X", "O"], ["", "O", "X"], ["", "X", ""]]
    current_player = "O"

    with pytest.raises(CellAlreadyFilled, match="Cell already filled. Please try again"):
        form = PlayerInputForm(data=form_data, game_board=game_board, current_player=current_player)
        form.is_valid()

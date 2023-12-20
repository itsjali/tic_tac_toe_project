import pytest
from unittest import mock
from django.test import RequestFactory
from django.http import HttpRequest
from game_app.views import play_game

@pytest.fixture
def mock_request():
    return RequestFactory().post('/play/')


def test_play_game_view_success_and_switch_players():
    request = HttpRequest()
    request.method = "POST"
    request.POST = {"row": 1, "col": 2}

    request.session = {"game_board": [["", "", ""], ["", "", ""], ["", "", ""]], "current_player": "O"}

    response = play_game(request)

    assert response.status_code == 200 
    assert request.session["game_board"] == "O" 
    assert request.session["current_player"] == "X"


def test_play_game_view_raise_value_error():
    request = HttpRequest()
    request.method = "POST"
    request.POST = {"row": 7, "col": 4}

    request.session = {"game_board": [["", "", ""], ["", "", ""], ["", "", ""]], "current_player": "O"}

    response = play_game(request)

    assert response.status_code == 200 
    assert "Unable to process your input" in response.content.decode("utf-8")
  

def test_play_game_view_raise_cell_already_filled_error():
    request = HttpRequest()
    request.method = "POST"
    request.POST = {"row": 1, "col": 2}

    request.session = {"game_board": [["", "X", ""], ["", "O", ""], ["X", "", ""]], "current_player": "O"}

    response = play_game(request)

    assert response.status_code == 200 
    assert "Cell already filled" in response.content.decode("utf-8")


def test_play_game_view_if_its_a_draw():
    request = HttpRequest()
    request.method = "POST"
    request.POST = {"row": 1, "col": 2}

    request.session = {"game_board": [["O", "", "O"], ["X", "O", "X"], ["X", "O", "O"]], "current_player": "X"}

    response = play_game(request)

    assert response.status_code == 200 
    assert "a Draw" in response.content.decode("utf-8")


@pytest.mark.parametrize(
    "game_board, user_input, player, winner",
    (
        ([["X", "X", ""], ["O", "O", ""], ["", "", ""]], {"row": 1, "col": 3}, "X", "Player 2"), # horizontal
        ([["O", "X", ""], ["O", "X", ""], ["", "", ""]], {"row": 3, "col": 1}, "O", "Player 1"), # vertical
        ([["X", "O", ""], ["O", "", ""], ["", "", "X"]], {"row": 2, "col": 2}, "X", "Player 2"), # diagonal
        ([["", "X", "O"], ["", "", ""], ["O", "X", "X"]], {"row": 2, "col": 2}, "O", "Player 1"), # opposite diagonal
    ),
)
def test_play_game_view_if_there_is_a_winner(game_board, user_input, player, winner):
    request = HttpRequest()
    request.method = "POST"
    request.POST = user_input

    request.session = {"game_board": game_board, "current_player": player}
    
    response = play_game(request)

    assert response.status_code == 200 
    assert f"{winner} Wins!" in response.content.decode("utf-8")


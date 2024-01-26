from django.core.validators import MaxValueValidator
from django.db import models


class GameBoard(models.Model):
    DEFAULT_BOARD = '[["", "", ""], ["", "", ""], ["", "", ""]]'
    data = models.CharField(default=DEFAULT_BOARD, max_length=50)


class Players(models.Model):
    SYMBOL_CHOICES = [
        ("O", "O"),
        ("X", "X"),
    ]

    player_game_id = models.IntegerField(default=1, validators=[MaxValueValidator(2)])
    symbol = models.CharField(max_length=1, choices=SYMBOL_CHOICES)
    game_board = models.ForeignKey(GameBoard, on_delete=models.CASCADE, related_name="players")

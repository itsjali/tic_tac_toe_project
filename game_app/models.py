from django.db import models

class GameData(models.Model):
    DEFAULT_BOARD = [["", "", ""], ["", "", ""], ["", "", ""]]
    
    board = models.CharField(default=DEFAULT_BOARD, max_length=50)
    current_player = models.CharField(max_length=1, default="O")

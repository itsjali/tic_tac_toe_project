from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    DEFAULT_BOARD = '[["", "", ""], ["", "", ""], ["", "", ""]]'
    board = models.CharField(default=DEFAULT_BOARD, max_length=50)
    
    player_1 = models.ForeignKey(User, related_name="player_1", on_delete=models.CASCADE, null=True)
    player_1_icon = models.CharField(max_length=1, default="O")
    player_2 = models.ForeignKey(User, related_name="player_2", on_delete=models.CASCADE, null=True)
    player_2_icon = models.CharField(max_length=1, default="X")
    active_player = models.ForeignKey(User, related_name="active_player", on_delete=models.CASCADE, null=True)
    
    is_active = models.BooleanField(default=True)
    outcome = models.CharField(max_length=10, null=True, blank=True)

    @property
    def has_active_game(self):
        """
        Return True if player_1 and player_2 already have an active Game.
        """
        existing_game = Game.objects.filter(
            player_1=self.player_1, 
            player_2=self.player_2, 
            is_active=True,
        )

        if existing_game:
            return True
        return False

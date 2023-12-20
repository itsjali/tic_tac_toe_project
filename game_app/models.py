# from django.db import models
# import json

# class GameBoard(models.Model):
#     cell_1 = models.CharField(max_length=3)
#     cell_2 = models.CharField(max_length=3)
#     cell_3 = models.CharField(max_length=3)
#     cell_4 = models.CharField(max_length=3)
#     cell_5 = models.CharField(max_length=3)
#     cell_6 = models.CharField(max_length=3)
#     cell_7 = models.CharField(max_length=3)
#     cell_8 = models.CharField(max_length=3)
#     cell_9 = models.CharField(max_length=3)


# class GameBoardDict(models.Model):
#     game_board_data = models.TextField(default='[["", "", ""], ["", "", ""], ["", "", ""]]')

#     def get_game_board(self):
#         return json.loads(self.game_board_data)
    
#     def update_cell(self, position, value):
#         row, col = position
#         game_board = self.get_game_board()
#         game_board[row][col] = value

#         self.game_board_data = json.dumps(game_board)
from django import forms 
from game_app.services import CellAlreadyFilled


class PlayerInputForm(forms.Form):
    row = forms.IntegerField() # can add a min and max 
    col = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        game_board = kwargs.pop("game_board", None)
        current_player = kwargs.pop("current_player", None)
        super(PlayerInputForm, self).__init__(*args, **kwargs)

        self.game_board = game_board
        self.current_player = current_player

    def clean(self):
        cleaned_data = super().clean()
        row = cleaned_data.get("row") - 1
        col = cleaned_data.get("col") - 1
        
        if not (0 <= row <= 2) or not (0 <= col <= 2):
            raise ValueError("Unable to process your input. Please input two valid numbers that are between 1-3")

        if self.game_board[row][col] != "":
            raise CellAlreadyFilled("Cell already filled. Please try again")

        cleaned_data["formatted_input"] = (row, col)
        return cleaned_data["formatted_input"]

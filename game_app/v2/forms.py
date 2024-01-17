from django import forms 

from game_app.v2.services import CellAlreadyFilled


class PlayerInputForm(forms.Form):
    row = forms.IntegerField(min_value=1, max_value=3)
    col = forms.IntegerField(min_value=1, max_value=3)

    def __init__(self, *args, **kwargs):
        game_board = kwargs.pop("game_board", None)
        super(PlayerInputForm, self).__init__(*args, **kwargs)

        self.game_board = game_board

    def clean(self):
        cleaned_data = super().clean()
        row = cleaned_data.get("row") - 1
        col = cleaned_data.get("col") - 1

        if self.game_board[row][col] != "":
            raise CellAlreadyFilled("Cell already filled. Please try again")

        cleaned_data["formatted_input"] = (row, col)
        return cleaned_data["formatted_input"]

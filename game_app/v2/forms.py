import json

from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from game_app.v2.services import (
    CellAlreadyFilled, 
    InvalidActiveUser,
    InvalidCredentials, 
    InvalidCreateUserCredentials,
)


class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100)
    password1 = forms.CharField(label="Password:", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password:", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data["username"]
        password1 = cleaned_data["password1"]
        password2 = cleaned_data["password2"]

        if User.objects.filter(username=username).exists():
            raise InvalidCreateUserCredentials("This username is already taken.")
        
        if password1 and password2:
            if password1 != password2:
                raise InvalidCreateUserCredentials("Passwords do not match.")
        
        user = User.objects.create_user(
            username=username,
            password=password1,
        )

        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise InvalidCredentials("Invalid username or password.")

            return user



class PlayerInputForm(forms.Form):
    row = forms.IntegerField(min_value=1, max_value=3)
    col = forms.IntegerField(min_value=1, max_value=3)

    def __init__(self, *args, **kwargs):
        game = kwargs.pop("game", None)
        user = kwargs.pop("user", None)
        super(PlayerInputForm, self).__init__(*args, **kwargs)

        self.game = game
        self.user = user

    def clean(self):
        if self.user != self.game.active_player:
            raise InvalidActiveUser("Please wait, it's not your turn yet.")

        cleaned_data = super().clean()
        row = cleaned_data.get("row") - 1
        col = cleaned_data.get("col") - 1
        
        game_board = json.loads(self.game.board)
        if game_board[row][col] != "":
            raise CellAlreadyFilled("Cell already filled. Please try again")

        cleaned_data["formatted_input"] = (row, col)
        return cleaned_data["formatted_input"]

# Welcome to my first Django Project 

#### A simple game of Tic Tac Toe. 

## Version 1

The game is played through a Python shell. 

To play this version, access your chosen terminal and navigate to the `v1` directory. 
```
cd game_app/v1/
python game.py 
```

Find your opponent and follow the prompt instructions. An input example: 
```
Player 1 - enter your move.
2 2
    |     |    
    |  O  |    
    |     |    
```

## Version 2

To play this version firstly, create and activate your virtual environment. Then install the dependancies. Here's an example on Linux: 
```
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt 
```

Run the Django server: 
```
python manage.py runserver
```

You should be able to access the development server `http://127.0.0.1:8000/`. 

To access the game you first need to sign up. Go to `http://127.0.0.1:8000/game/signup/`, add your credentials. The database is only for local environment so if you want to play against someone they would need to create a user in your server. 

Easiest way you can do this is by using ngrok. First install ngrok if you haven't already. Then you would need to run `ngrok http 8000` in your terminal, copy the forwarding url and paste it in the `ALLOWED_HOSTS` variable in the `settings.py`. Your variable should look like this for example: `ALLOWED_HOSTS = ['3c45-2a00-23c7-2c0e-9301-729c-9d68-8b90-ed64.ngrok-free.app']`

Give your opponent the ngrok url with the trailing path components `/game/signup/`. 

Once you and your opponent have signed up, you are ready to play. You will be asked to sign in then you are redirected to the home screen. Under `Play Against` you are able to click on your opponent's username. This should redirect you the game where you are able to input moves to start playing. Note: your opponent would need to refresh their browser, under `Active Games` they should be able to see your username where they can click to start playing against you.

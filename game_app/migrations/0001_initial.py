# Generated by Django 3.2.12 on 2024-01-24 19:14

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(default='[["", "", ""], ["", "", ""], ["", "", ""]]', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_game_id', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(2)])),
                ('symbol', models.CharField(choices=[('O', 'O'), ('X', 'X')], max_length=1)),
                ('game_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='game_app.gameboard')),
            ],
        ),
    ]

# Generated by Django 3.2.12 on 2023-12-20 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.CharField(default=[['', '', ''], ['', '', ''], ['', '', '']], max_length=50)),
                ('current_player', models.CharField(default='O', max_length=1)),
            ],
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-14 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duduapp', '0003_movie_notes_alter_movie_bubu_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='type',
            field=models.CharField(choices=[('movie', 'Movie'), ('tv-show', 'TV Show')], default='movie', max_length=7),
        ),
    ]

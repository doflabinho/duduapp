# Generated by Django 5.1.1 on 2024-10-18 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duduapp', '0007_dateimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='dateimage',
            name='title',
            field=models.CharField(default='Untitled', max_length=100),
            preserve_default=False,
        ),
    ]

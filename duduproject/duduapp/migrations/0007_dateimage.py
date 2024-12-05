# Generated by Django 5.1.1 on 2024-10-18 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('duduapp', '0006_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='date_images/')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='duduapp.date')),
            ],
        ),
    ]
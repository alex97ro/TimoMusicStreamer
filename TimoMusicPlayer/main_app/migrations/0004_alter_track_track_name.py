# Generated by Django 4.2.10 on 2024-02-18 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_remove_track_track_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='track_name',
            field=models.CharField(max_length=100),
        ),
    ]

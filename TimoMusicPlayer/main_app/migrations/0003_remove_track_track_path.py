# Generated by Django 4.2.10 on 2024-02-18 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_playlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='track_path',
        ),
    ]

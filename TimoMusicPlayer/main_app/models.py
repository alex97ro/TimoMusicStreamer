from django.db import models
from django.db.models import SET_NULL
from pytubefix import YouTube
from pytubefix import Search


class Track(models.Model):
    track_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    track_url = models.URLField()
    thumbnail_url = models.URLField()

    def __str__(self):
        return self.track_name

    @staticmethod
    def search_track(track_name):
        search_results = Search(track_name)
        return search_results.results


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    tracks = models.ManyToManyField(to='main_app.Track', related_name='playlists', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


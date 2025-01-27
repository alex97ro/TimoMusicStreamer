from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from main_app.models import Track, Playlist


def index(request):
    return render(request, 'main_app/index.html')


def playlists(request):
    playlists = Playlist.objects.all()
    return render(request, 'main_app/playlists.html', context={'playlists': playlists})


def playlist(request, playlist_id):
    playlist_object = Playlist.objects.get(id=playlist_id)
    tracks = playlist_object.tracks.all()
    return render(request, 'main_app/playlist.html', context={'tracks': tracks})

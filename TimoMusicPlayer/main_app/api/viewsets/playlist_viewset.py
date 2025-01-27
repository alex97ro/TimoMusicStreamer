from rest_framework import viewsets
from main_app.models import Playlist
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()

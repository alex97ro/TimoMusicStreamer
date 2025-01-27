from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('playlists', views.playlists, name='playlists'),
    path('playlist/<int:playlist_id>', views.playlist, name='playlist'),
]
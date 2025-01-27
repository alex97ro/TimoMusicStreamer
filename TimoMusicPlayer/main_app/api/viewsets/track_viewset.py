from django.http import JsonResponse, HttpResponse
from main_app.models import Track, Playlist
from main_app.api.serializers import TrackSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from io import BytesIO
from pytube import YouTube
from pytube import Search

from rest_framework.response import Response


class TrackViewSet(viewsets.ModelViewSet):
    serializer_class = TrackSerializer
    queryset = Track.objects.all()

    @action(methods=['get'], detail=False, url_name='get-search-results')
    def get_search_results(self, request):
        track_string = request.query_params.get('track_string')
        if track_string is None:
            return JsonResponse({'message': 'No track title provided'}, status=status.HTTP_404_NOT_FOUND)
        else:
            results = Track.search_track(track_string)
            if results:
                result_json = {
                    f'{index}': {'title': results[index].title, 'thumbnail_url': results[index].thumbnail_url,
                                 'author': results[index].author, 'track_url': results[index].watch_url}
                    for index in range(10)}

                return JsonResponse(result_json, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'No results found'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], url_name='select_track', url_path='select-track', detail=False)
    def select_track(self, request):
        track_string = request.query_params.get('track_string')
        results = Track.search_track(track_string)
        track = results[0]
        streams = track.streams.filter(only_audio=True)
        stream = streams[0]
        print(stream)
        buffer = BytesIO()
        stream.stream_to_buffer(buffer)
        print(buffer.__sizeof__())
        response = HttpResponse(buffer.getvalue(), content_type='video/mp4')

        # Optionally, set the content disposition header to prompt download
        response['Content-Disposition'] = f'attachment; filename="{track_string}.mp4"'
        return response

    @action(methods=['post'], detail=False, url_path='add-playlist', url_name='add_playlist')
    def add_playlist(self, request):
        playlist_name = request.data.get('playlist_name')
        if Playlist.objects.filter(name=playlist_name).exists():
            return JsonResponse({'message': 'Playlist with this name already exists'}, status=status.HTTP_409_CONFLICT)
        else:
            new_playlist = Playlist(name=playlist_name)
            new_playlist.save()
            return JsonResponse({'message': 'Playlist created successfully'}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_name='add_track', url_path='add-track')
    def add_track(self, request, pk=None):
        try:
            playlist = Playlist.objects.get(id=pk)
        except Playlist.DoesNotExist as exc:
            return JsonResponse({'exception': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        else:
            track_url = request.data.get('track_url')
            track, created = Track.objects.get_or_create(track_url=track_url)
            if created:
                track_name = request.data.get('track_name')
                thumbnail_url = request.data.get('thumbnail_url')
                track.track_name = track_name
                track.thumbnail_url = thumbnail_url
                track.save()
                playlist.tracks.add(track)
                return JsonResponse({'message': 'Track was added successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Track is already added'}, status=status.HTTP_409_CONFLICT)

    @action(methods=['get'], detail=True, url_name='play_track',url_path='play-track')
    def play_track(self, request, pk=None):
        try:
            track = Track.objects.get(id=pk)
        except Track.DoesNotExist as exc:
            return JsonResponse({'exception': str(exc)}, status=status.HTTP_404_NOT_FOUND)
        else:
            yt = YouTube(url=track.track_url)
            streams = yt.streams.filter(only_audio=True).filter(file_extension='mp4')
            stream = streams[0]
            print(stream)
            buffer = BytesIO()
            stream.stream_to_buffer(buffer)
            print(buffer.__sizeof__())
            response = HttpResponse(buffer.getvalue(), content_type='video/mp4')
from rest_framework import routers
from main_app.api import viewsets

main_app_router = routers.DefaultRouter()
main_app_router.register('tracks', viewsets.TrackViewSet)

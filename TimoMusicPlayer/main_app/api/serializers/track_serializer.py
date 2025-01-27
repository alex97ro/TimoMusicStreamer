from main_app.models import Track
from rest_framework import serializers


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"

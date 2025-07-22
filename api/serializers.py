from rest_framework import serializers
from .models import Playlist, Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'length', 'date_released', 'price']
        read_only_fields = ['id']

class PlaylistSerializer(serializers.ModelSerializer):
    songs = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Song.objects.all()
    )

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'songs']
        read_only_fields = ['id']
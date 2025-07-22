from django.db import models
import random

class Song(models.Model):
    title = models.CharField(max_length=255)
    length = models.PositiveIntegerField(help_text="Length in seconds")
    date_released = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
    
class Playlist(models.Model):
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name='playlists')

    def __str__(self):
        return self.name

    def shuffle_songs(self):
        song_list = list(self.songs.all())
        random.shuffle(song_list)
        return song_list
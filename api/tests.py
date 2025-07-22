from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Song, Playlist

class SongAPITestCase(APITestCase):

    def setUp(self):
        self.song1 = Song.objects.create(title="Song 1", length=200, date_released="2022-01-01T00:00:00Z", price=4.00)
        self.song2 = Song.objects.create(title="Song 2", length=150, date_released="2023-01-01T00:00:00Z", price=6.00)
        self.song3 = Song.objects.create(title="Song 3", length=180, date_released="2021-01-01T00:00:00Z", price=12.00)

    # CRUD Tests

    def test_list_songs(self):
        url = reverse('song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_song(self):
        url = reverse('song-list')
        data = {
            "title": "New Song",
            "length": 240,
            "date_released": "2023-05-01T00:00:00Z",
            "price": 5.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Song.objects.count(), 4)

    def test_retrieve_song(self):
        url = reverse('song-detail', args=[self.song1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Song 1")

    def test_update_song(self):
        url = reverse('song-detail', args=[self.song1.id])
        data = {
            "title": "Updated Song",
            "length": 200,
            "date_released": "2022-01-01T00:00:00Z",
            "price": 4.00
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.song1.refresh_from_db()
        self.assertEqual(self.song1.title, "Updated Song")

    def test_delete_song(self):
        url = reverse('song-detail', args=[self.song1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Song.objects.count(), 2)

    # Purchase Tests

    def test_purchase_with_cheap_gateway(self):
        url = reverse('purchase')
        data = {
            "songs": [self.song1.id, self.song2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_price"], 10.00)

    def test_purchase_with_expensive_gateway(self):
        url = reverse('purchase')
        data = {
            "songs": [self.song3.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_price"], 12.00)

    # Playlist Tests

    def test_create_playlist(self):
        url = reverse('playlist-list')
        data = {
            "name": "My Playlist",
            "songs": [self.song1.id, self.song2.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_shuffle_playlist(self):
        playlist = Playlist.objects.create(name="Shuffle Test")
        playlist.songs.set([self.song1, self.song2, self.song3])
        url = reverse('playlist-shuffle', args=[playlist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        returned_ids = [song["id"] for song in response.data] 
        expected_ids = [self.song1.id, self.song2.id, self.song3.id]
        self.assertEqual(set(returned_ids), set(expected_ids))
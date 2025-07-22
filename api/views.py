from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Playlist, Song
from .serializers import PlaylistSerializer, SongSerializer

# Payment gateway classes directly in views.py
class CheapPaymentGateway:
    @staticmethod
    def process_payment(amount):
        # Simulate cheap payment processing
        print(f"Processing cheap payment for amount: {amount}")
        return True

class ExpensivePaymentGateway:
    @staticmethod
    def process_payment(amount):
        # Simulate expensive payment processing
        print(f"Processing expensive payment for amount: {amount}")
        return True

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class PurchaseView(APIView):
    def post(self, request):
        song_ids = request.data.get('songs', [])
        if not song_ids or not isinstance(song_ids, list):
            return Response({"error": "Provide a list of song IDs under 'songs' key."},
                            status=status.HTTP_400_BAD_REQUEST)

        songs = Song.objects.filter(id__in=song_ids)
        if songs.count() != len(song_ids):
            return Response({"error": "One or more song IDs are invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(song.price for song in songs)

        if total_price < 10:
            success = CheapPaymentGateway.process_payment(total_price)
        else:
            success = ExpensivePaymentGateway.process_payment(total_price)

        if success:
            return Response({
                "message": "Payment processed successfully.",
                "total_price": total_price,
                "songs_purchased": SongSerializer(songs, many=True).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Payment failed."},
                            status=status.HTTP_402_PAYMENT_REQUIRED)
        
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer

    @action(detail=True, methods=['get'])
    def shuffle(self, request, pk=None):
        playlist = self.get_object()
        shuffled_songs = playlist.shuffle_songs()
        # Serialize songs to return
        from .serializers import SongSerializer
        serializer = SongSerializer(shuffled_songs, many=True)
        return Response(serializer.data)
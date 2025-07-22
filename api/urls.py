from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PlaylistViewSet, SongViewSet, PurchaseView

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet)

urlpatterns = router.urls + [
    path('purchase/', PurchaseView.as_view(), name='purchase'),
]
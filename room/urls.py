from rest_framework.routers import DefaultRouter

from room.views import RoomViewSet

router = DefaultRouter()
router.register(r"room", RoomViewSet, basename="room-admin")
router.register(r"p/room", RoomViewSet, basename="room-public")
urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from accommodation.views import RoomViewSet, RoomPublicViewSet, FlatViewSet, FlatPublicViewSet

router = DefaultRouter()
router.register(r"room", RoomViewSet, basename="room-admin")
router.register(r"p/room", RoomPublicViewSet, basename="room-public")
router.register(r"flat", FlatViewSet, basename="flat-admin")
router.register(r"p/flat", FlatPublicViewSet, basename="flat-public")
urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from accommodation.views import (
    AdminRoomViewSet,
    PublicRoomViewSet,
    AdminFlatViewSet,
    PublicFlatViewSet,
    AdminHouseViewSet,
    PublicHouseViewSet,
)

router = DefaultRouter()

router.register(r"room", AdminRoomViewSet, basename="room-admin")
router.register(r"p/room", PublicRoomViewSet, basename="room-public")
router.register(r"flat", AdminFlatViewSet, basename="flat-admin")
router.register(r"p/flat", PublicFlatViewSet, basename="flat-public")
router.register(r"house", AdminHouseViewSet, basename="house-admin")
router.register(r"p/house", PublicHouseViewSet, basename="house-public")

urlpatterns = router.urls

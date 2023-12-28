from rest_framework.routers import DefaultRouter

from media.views import MediaViewSet

router = DefaultRouter()
router.register(r"media", MediaViewSet, basename="media-admin")
urlpatterns = router.urls

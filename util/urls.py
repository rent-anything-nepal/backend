from django.urls import path
from rest_framework.routers import DefaultRouter

from util.views import MediaViewSet, ContentTypesView

router = DefaultRouter()
router.register(r"media", MediaViewSet, basename="media-admin")
urlpatterns = router.urls

urlpatterns += [
    path("content-types/", ContentTypesView.as_view(), name="content-types"),
]

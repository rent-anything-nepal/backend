from rest_framework.routers import DefaultRouter

from review.views import ReviewViewSet, QAndAViewSet

router = DefaultRouter()
router.register(r"review", ReviewViewSet, basename="review-admin")
router.register(r"qna", QAndAViewSet, basename="qna-admin")
urlpatterns = router.urls

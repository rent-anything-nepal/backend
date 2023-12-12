from rest_framework.routers import DefaultRouter

from insight.views import ReviewViewSet, QAndAViewSet, RuleViewSet

router = DefaultRouter()
router.register(r"review", ReviewViewSet, basename="review-admin")
router.register(r"qna", QAndAViewSet, basename="qna-admin")
router.register(r"rule", QAndAViewSet, basename="rule-admin")
urlpatterns = router.urls

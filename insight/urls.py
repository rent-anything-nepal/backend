from django.urls import path
from rest_framework.routers import DefaultRouter

from insight.views import ReviewViewSet, QAndAViewSet, RuleViewSet, SavedSearchView

router = DefaultRouter()
router.register(r"review", ReviewViewSet, basename="review-admin")
router.register(r"qna", QAndAViewSet, basename="qna-admin")
router.register(r"rule", RuleViewSet, basename="rule-admin")
urlpatterns = router.urls

urlpatterns += [
    path("saved-search/", SavedSearchView.as_view(), name="saved_search")
]

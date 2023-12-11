from django.urls import path
from rest_framework.routers import DefaultRouter

from account.views import (
    UserViewSet,
    RegisterUserView,
    LoginView,
    LogoutView,
    RetrieveMeView,
    UpdatePasswordView,
    RequestPasswordResetView,
    ConfirmPasswordResetView,
)

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user-admin")
urlpatterns = router.urls

urlpatterns += [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", RetrieveMeView.as_view()),
    path("update-password/", UpdatePasswordView.as_view()),
    path("request-password-reset/", RequestPasswordResetView.as_view()),
    path("confirm-password-reset/<str:code>/", ConfirmPasswordResetView.as_view()),
]

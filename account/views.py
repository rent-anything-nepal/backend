from os import getenv

from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_condition import And
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from account.models import ResetPasswordCode
from account.permissions import IsSuperUser
from account.serializers import (
    UserSerializer,
    LoginSerializer,
    LogoutSerializer,
    RequestResetPasswordSerializer,
    UpdatePasswordSerializer,
    ResetPasswordSerializer,
)

from dotenv import load_dotenv


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_fields = [
        "is_staff",
        "is_superuser",
        "is_active",
        "profile__account_type",
        "profile__is_citizenship_verified",
        "profile__is_contact_verified",
        "profile__is_email_verified",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "profile__citizenship_number",
        "middle_name",
        "profile__primary_contact",
        "profile__secondary_contact",
        "profile__address",
        "profile__city",
    ]
    permission_classes = [And(IsSuperUser, IsAuthenticated)]


class RegisterUserView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        payload = request.data
        serializer = UserSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        payload = request.data
        serializer = LoginSerializer(data=payload)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"], password=serializer.validated_data["password"]
        )
        if user is None:
            return Response({"error": "Invalid username/password"}, status=401)
        user.last_login = timezone.now()
        if not user.is_active:
            user.is_active = True
        user.save()

        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)

        return Response({"token": token.key, "user": UserSerializer(user).data})


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_model().objects.get(username=serializer.validated_data["username"])
        if user is None:
            return Response({"error": "Invalid username"}, status=401)
        Token.objects.filter(user=user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RetrieveMeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UpdatePasswordView(APIView):
    def post(self, request):
        user = request.user
        serializer = UpdatePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data.get("old_password")):
            return Response({"details": ["Invalid old password"]}, status=400)
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        Token.objects.filter(user=user).delete()
        return Response(status=204)

    def delete(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        user.delete()
        return Response(status=204)


class RequestPasswordResetView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = RequestResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_user_model().objects.get(email=serializer.validated_data["email"])
        if user is None:
            return Response({"error": "Invalid email"}, status=401)

        reset_code = ResetPasswordCode.objects.filter(user=user, is_used=False, is_expired=False).first()
        if reset_code:
            if reset_code.has_expired():
                reset_code.expire()
        else:
            reset_code = ResetPasswordCode.objects.create(user=user)

        load_dotenv()
        send_mail(
            "Request Reset Password",
            message="ResetPassword",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=render_to_string(
                "request_reset_password.html",
                {
                    "username": user.username,
                    "code": reset_code.code,
                    "host": request.get_host(),
                    "scheme": request.scheme,
                    "frontend_host": getenv("FRONTEND_HOST"),
                },
            ),
        )
        return Response(status=204)


class ConfirmPasswordResetView(APIView):
    def post(self, request, code):
        reset_code = ResetPasswordCode.objects.filter(code=code, is_used=False, is_expired=False).first()
        if not reset_code:
            return Response(404)
        if reset_code.has_expired():
            return Response({"details": "Reset code has been expired."}, status=403)
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = reset_code.user
        user.set_password(serializer.validated_data.get("new_password"))
        user.save()
        Token.objects.filter(user=user).delete()
        reset_code.is_used = True
        reset_code.save()
        return Response(200)

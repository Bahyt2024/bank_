from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.activation_link = str(uuid.uuid4())
        user.save()

        # Генерация ссылки активации
        activation_url = f"http://localhost:8000/api/auth/activate/{user.activation_link}"

        # Отправка email
        send_mail(
            subject="Активация аккаунта",
            message=f"Пройдите по ссылке для активации аккаунта: {activation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({"message": "Пользователь зарегистрирован, проверьте почту для активации"})

class ActivateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, link):
        user = get_object_or_404(User, activation_link=link)
        user.is_activated = True
        user.activation_link = None
        user.save()
        return Response({"message": "Аккаунт активирован"})

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        RefreshToken(request.data["refresh"]).blacklist()
        return Response({"message": "Вы вышли из системы"})

class UsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role != 'admin':
            return Response({"detail": "Недостаточно прав"}, status=403)
        users = User.objects.all().values('id', 'email', 'first_name', 'last_name', 'role', 'is_blocked')
        return Response(users)

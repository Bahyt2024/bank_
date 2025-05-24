from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])

        if user is None:
            raise serializers.ValidationError("Неверный email или пароль")
        if not user.is_activated:
            raise serializers.ValidationError("Аккаунт не активирован")
        if user.is_blocked:
            raise serializers.ValidationError("Аккаунт заблокирован")

        refresh = RefreshToken.for_user(user)
        return {
            'user': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
